"""
Author: Bishal Samanta

This module serves as the entry point for the model training pipeline.
It processes an RNA sequence dataset received as a Pandas DataFrame from the frontend(uploaded by the admin as a CSV file).
or loads the data from a CSV file (original dataset) when run locally for the first time.
The module extracts sequence-based features using the ViennaRNA package, preprocesses the data,
and trains a stacking model combining RandomForest and XGBoost.
It then evaluates the model's performance and saves the trained model to a file.
Additionally, it visualizes feature distributions and stores the generated plots in a specified directory.

"""


# Importing required libraries
import RNA
import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import pickle
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Backend/rna_model.log'),# Log file
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Function to check if the data is valid
def check_data(df):

    """
    Check the input data for completeness and validity. This is done by checking the required columns, na values, and duplicate rows.
    We also check if the sequences contain valid nucleotides (A, U, C, G) (necessary check for biological sequences ).
    Args:
        df (pd.DataFrame): Input DataFrame containing RNA sequences and efficacy values.
    Returns:
        pd.DataFrame: DataFrame with valid data after performing checks.

    """

    try:
        # Check if the DataFrame is empty or None
        if df is None or df.empty:
            raise ValueError("The DataFrame is empty or None.")
        
        logger.info(f"Data loaded.....performing checks on the data. Shape:{df.shape}")
        
        # Check for required columns
        required_columns = {"gRNA_PAM", "efficacy"}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Missing required columns. Expected columns: {required_columns}")
                
        # Drop missing values
        df = df.dropna()

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Check for valid nucleotide sequences
        valid_nucleotides_pattern = re.compile(r"^[ATCG]+$", re.IGNORECASE)
        df = df[df['gRNA_PAM'].apply(lambda x: isinstance(x, str) and bool(valid_nucleotides_pattern.match(x)))]
        logger.info(f"Input Data checks done.......Shape:{df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error while data checks: {str(e)}")
        sys.exit(1)  # Exit if data is not valid

# Function to calculate features for a single RNA sequence
def calculate_features(seq):
    
    """
    Enrich the sequences with biological features using the ViennaRNA package.
    The function calculates the following features for an sequence:
    1. Minimum free energy (MFE) of the secondary structure.
    2. Base-pairing probabilities.
    3. Thermodynamic properties using ensemble free energy.
    4. Sequence-based features using one-hot encoding.
    5. Structural properties like number of helices, average helix length, and fraction of paired bases.
    All the features serve as input to the machine learning model for our prediction task.
    Args:
        seq (str): RNA sequence.
    Returns:
        list: List of features calculated for the sequence.

    """

    try:
        # 1. Minimum free energy (MFE)
        (ss, mfe) = RNA.fold(seq)

        #2. Base-pairing probabilities
        fc = RNA.fold_compound(seq)
        (pp, pf) = fc.pf()
        bp_probs = fc.bpp()
        avg_bp_prob = np.mean([bp_probs[i][j] for i in range(len(seq)) for j in range(i+1, len(seq)) if i < j])

        # 3. Thermodynamic properties (using ensemble free energy)
        ensemble_energy = fc.mean_bp_distance()
        
        # 4. Sequence-based features (one-hot encoding)
        bases = ['A', 'U', 'C', 'G']
        one_hot = np.array([[1 if seq[i] == b else 0 for b in bases] for i in range(len(seq))]).flatten()
        
        # 5. Structural properties
        helices, paired_bases, in_helix, current_helix_length, helix_lengths = 0, 0, False, 0, []
        
        for char in ss:
            if char == '(':
                paired_bases += 1
                if not in_helix:
                    helices += 1
                    in_helix = True
                current_helix_length += 1
            elif char == ')':
                paired_bases += 1
                current_helix_length += 1
            else:
                if in_helix:
                    helix_lengths.append(current_helix_length)
                    current_helix_length = 0
                    in_helix = False
        
        if in_helix:
            helix_lengths.append(current_helix_length)
        
        avg_helix_length = np.mean(helix_lengths) if helix_lengths else 0
        fraction_paired = paired_bases / len(seq)
        
        return [mfe, avg_bp_prob, ensemble_energy] + list(one_hot) + [helices, avg_helix_length, fraction_paired]
    except Exception as e:
        logger.error(f"Error calculating features for sequence: {seq}. Error: {str(e)}")
        return None

# Function to extract features from RNA sequences
def extract_features(df):

    """
    Extract features from RNA sequences using the ViennaRNA package.
    We calculate features for each RNA sequence in the DataFrame using the calculate_features function and 
    combine them into a single DataFrame using the feature names.
    Args:
        df (pd.DataFrame): DataFrame containing RNA sequences.
    Returns:
        pd.DataFrame: DataFrame containing calculated features for each sequence.
    """

    logger.info("Extracting features for RNA sequences...")
    # Calculate features for each sequence
    features = df['gRNA_PAM'].apply(calculate_features)
    if features.isnull().any():
        logger.error("Feature calculation failed for one or more sequences.")
        sys.exit(1)
    feature_names = ['MFE', 'Avg_BP_Prob', 'Ensemble_Energy'] +[f'OneHot_{i}' for i in range(92)] + ['Helices', 'Avg_Helix_Length',
                                                                                                      'Fraction_Paired']
    return pd.DataFrame(features.tolist(), columns=feature_names)

# Function to preprocess data (impute missing values and scale features)
def preprocess_data(X):

    """
    Preprocess features by imputing missing values and scaling features.
    The missing values are imputed with the mean of the column and the features are scaled using StandardScaler.
    This ensures uniformity in the scale of the features.
    Args:
        X (pd.DataFrame): DataFrame containing features.
    Returns:    
        np.ndarray: Preprocessed features.

    """

    try:
        logger.info("Starting data preprocessing...")
        
        # Impute missing values with mean
        imputer = SimpleImputer(strategy='mean')
        X = imputer.fit_transform(X)
        
        # Scale features using StandardScaler
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        logger.info("Data Preprocessing Completed.")
        
        return X
    except Exception as e:
        logger.error(f"Error during data preprocessing: {str(e)}")
        sys.exit(1)

# Function to train a stacking model
def train_model(X_train, y_train):

    """
    Create the base models Random Forest and XGBoost.The models are trained using the  default hyperparameters.
    After creating the base models we use a Linear Regression model as the final estimator for our stacking ensemble model.
    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target values.
    Returns:
        StackingRegressor: Trained stacking model.  

    """

    logger.info("Training model...")
    try:
        # Define base models and stacking model
        base_models = [('random_forest', RandomForestRegressor(random_state=42)),
                        ('xgboost', XGBRegressor(random_state=42))] # Keep the random_state constant for reproducibility
        stacking_model = StackingRegressor(estimators=base_models, final_estimator=LinearRegression(), n_jobs=-1)
        stacking_model.fit(X_train, y_train)
        logger.info("Model training completed.")
        return stacking_model
    except Exception as e:
        logger.error(f"Error during model training: {str(e)}")
        sys.exit(1)

# Function to save trained model to a file
def save_model(model, file_path='Backend/stacking_model.pkl'):

    """ 
    Save the trained model to a file. The model is saved using the pickle module.
    This allows us to load the model later for making predictions on new data saving the time of retraining the model.
    Args:
        model: Trained model object.
        file_path (str): File path to save the model.
    Returns:
        None    

    """
    logger.info("Saving model...")
    try:
        # Save model to a file
        with open(file_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Model saved as {file_path}.")
        f.close()
    except Exception as e:
        logger.error(f"Error saving the model: {str(e)}")
        sys.exit(1)

# Function to evaluate model performance
def evaluate_model(model, X_test, y_test):

    """
    Evaluate the trained model using test data.
    Calculating the mean squared error (MSE), mean absolute error (MAE), and R-squared score.
    These metrics help us understand how well the model is performing on unseen data.
    Args:
        model: Trained model object.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): Test target values.
    Returns: 
        np.ndarray: Predicted target values.
        float: Mean squared error.
        float: Mean absolute error.
        float: R-squared score.

    """ 

    logger.info("Evaluating model...")
    try:
        # Make predictions
        y_pred = model.predict(X_test)
        # Calculate evaluation metrics
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        logger.info(f"MSE: {mse}, MAE: {mae}, R2: {r2}")
        return y_test, y_pred, mse, mae, r2
    except Exception as e:
        logger.error(f"Error during evaluation: {str(e)}")
        sys.exit(1)

# Function to visualize and save feature distributions (excluding one-hot encoded features)
def visualize_features(X, output_dir='Backend/feature_plots'):

    """
    Visualize and save feature distributions.
    Histograms are plotted for each feature to understand the distribution of the features.
    The plots are saved to a directory for further analysis.
    Args:
        X (pd.DataFrame): DataFrame containing features.
        output_dir (str): Directory to save the plots.  
    Returns:
        None

    """

    try:
        logger.info("Visualizing feature distributions...")

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Exclude one-hot encoded features (columns starting with 'OneHot_')
        features_to_plot = [col for col in X.columns if not col.startswith('OneHot_')]

        # Plot distributions for each feature
        for feature in features_to_plot:
            plt.figure(figsize=(8, 6))
            sns.histplot(X[feature], kde=True)
            plt.title(f'Distribution of {feature}')
            plt.xlabel(feature)
            plt.ylabel('Frequency')
            plt.savefig(os.path.join(output_dir, f'{feature}_distribution.png'))
            plt.close()
            logger.debug(f"Saved plot for feature: {feature}")

        logger.info(f"Feature plots saved in directory: {output_dir}")

    except Exception as e:
        logger.error(f"Error during feature visualization: {str(e)}")
        sys.exit(1)

# Function to visualize and save residual plot
def visualize_residualplot(y_test, y_pred,output_dir='Backend/feature_plots'):

    """ 
    The residual plot is a scatter plot of the actual target values vs the predicted target values.
    This plot helps us understand the anlyse the performance of the model and check if the errors are randomly distributed.
    The plot is saved to a directory for further analysis.
    Args:
        y_test (np.ndarray): Test target values.
        y_pred (np.ndarray): Predicted target values.
        output_dir (str): Directory to save the plot.
    Returns:
        None

    """

    try:
        logger.info("Visualizing residual plot...")

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Plot residual plot
        plt.figure(figsize=(8, 6))
        plt.scatter(y_test, y_pred)
        plt.xlabel('Actual Efficacy')
        plt.ylabel('Predicted Efficacy')
        plt.title('Actual vs Predicted Efficacy')
        plt.savefig(os.path.join(output_dir, 'residual_plot.png'))        


        logger.info("Residual plot saved.")

    except Exception as e:
        logger.error(f"Error during residual plot visualization: {str(e)}")
        sys.exit(1)

# Main function
def main(df):

    """
    Main function to run the model training pipeline.
    The dataframe is passed from the frontend and the model is trained using the RNA sequences and efficacy values.
    This part is used when the admin wants to update the model with new data.
    For normal prediction purposes the model is loaded from the file.
    Args:
        df (pd.DataFrame): Input DataFrame containing RNA sequences and efficacy values.
    Returns:
        float: Mean squared error of the model.
        float: Mean absolute error of the model.
        float: R-squared score of the model.

    """
        
    logger.info("Starting model training pipeline...")
    # Check  input data    
    df = check_data(df)
    # Extract features
    X = extract_features(df)
    # Extract efficacy values
    y = df['efficacy']
    # Visualize feature distributions
    visualize_features(X)
    # Preprocess data
    X_preprocessed = preprocess_data(X)
    # Split data(Training(80%) and Testing(20%))
    X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y,
                                                         test_size=0.2, random_state=42) # Keep the random_state constant for reproducibility
    # Train model
    model = train_model(X_train, y_train)
    # Save model
    save_model(model)
    # Evaluate model
    y_test, y_pred, mse, mae, r2 = evaluate_model(model, X_test, y_test)
    
    # Visualize residual plot
    visualize_residualplot(y_test, y_pred)

    logger.info("Model training pipeline completed.")
    # Return evaluation metrics
    return mse, mae, r2

# Unit Test
# Function to test the generate the model locally(only for testing purposes)
# make sure to comment the below code before deploying to the server
# Also make sure to see if the dataset is present in the correct path
# Uncomment the below code to test it locally
"""
def test_main():

    try:
        file_path = os.path.join('Backend', 'data_enc.csv')
        df = pd.read_csv(file_path, encoding="utf-8")
        main(df)
    except FileNotFoundError:
        print("Error: The file 'data_enc.csv' was not found. Check the file path.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: Error parsing the CSV file. Check for incorrect delimiters.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
"""
# End of code
