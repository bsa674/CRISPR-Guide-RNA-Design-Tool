"""
Script to predict efficacy scores for k-mers using a saved model. The k-mers are generated form the user specified input 
and after calculating the features, the model is used to predict the efficacy scores. The predicted scores are then shown to the user.
The script also contains various visualization functions for the feature distributions and correlations.
Authors: Zeynep Aslan and Mateo Carvajal
"""

# Importing required libraries
import RNA
import pandas as pd
import numpy as np
import pickle
import logging
import plotly.express as px
import plotly.graph_objects as go
from traceback import print_exc
# Zeynep Aslan
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Backend/kmer_prediction.log'),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

# Function to generate k-mers
def generate_kmers(sequence, k=23):

    """
    Function to generate k-mers from a given DNA sequence of length 23 that ends with AG, GG, or GA.
    The input data is cleaned by removing newline characters. Then k-mers of length k are generated from the sequence and
    check for valid sequences that end with AG, GG, or GA.
    Args:
        sequence (str): Input DNA sequence
        k (int): Length of k-mers to generate (default=23)
    Returns:
        kmers (list): List of k-mers that end with AG, GG, or GA

    """
    sequence = sequence.replace('\n', '')
    kmers = []
    suffixes = {'AG', 'GG', 'GA'}
    valid_bases = {'A', 'T', 'C', 'G'}
    
    # Ensure the sequence is long enough to generate k-mers of length k
    if len(sequence) < k:  
        return kmers
    
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        
        # Check if all characters in the k-mer are valid DNA bases
        if set(kmer).issubset(valid_bases) and kmer[-2:] in suffixes:
            kmers.append(kmer)
    
    return kmers


# Function to calculate features for a single RNA sequence
def calculate_features(seq):
    
    """
    Function to calculate features for a single RNA sequence.
    Args:
        seq (str): RNA sequence
    Returns:
        features (list): List of calculated features

    """

    try:
        logger.debug(f"Calculating features for sequence: {seq}")

        # 1. Minimum free energy (MFE)
        (ss, mfe) = RNA.fold(seq)
        logger.debug(f"Secondary structure: {ss}, MFE: {mfe}")

        # 2. Base-pairing probabilities
        fc = RNA.fold_compound(seq)
        (pp, pf) = fc.pf()
        bp_probs = fc.bpp()
        avg_bp_prob = np.mean([bp_probs[i][j] for i in range(len(seq)) for j in range(i+1, len(seq)) if i < j])
        logger.debug(f"Average base-pairing probability: {avg_bp_prob}")

        # 3. Thermodynamic properties (using ensemble free energy)
        ensemble_energy = fc.mean_bp_distance()
        logger.debug(f"Ensemble energy: {ensemble_energy}")

        # 4. Sequence-based features (one-hot encoding)
        bases = ['A', 'U', 'C', 'G']
        one_hot = np.array([[1 if seq[i] == b else 0 for b in bases] for i in range(len(seq))]).flatten()
        logger.debug(f"One-hot encoding: {one_hot}")

        # 5. Structural properties
        helices = 0
        helix_lengths = []
        paired_bases = 0
        in_helix = False
        current_helix_length = 0

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
            else:  # unpaired base
                if in_helix:
                    helix_lengths.append(current_helix_length)
                    current_helix_length = 0
                    in_helix = False

        if in_helix:
            helix_lengths.append(current_helix_length)

        avg_helix_length = np.mean(helix_lengths) if helix_lengths else 0
        fraction_paired = paired_bases / len(seq)
        logger.debug(f"Helices: {helices}, Avg helix length: {avg_helix_length}, Fraction paired: {fraction_paired}")

        return [mfe, avg_bp_prob, ensemble_energy] + list(one_hot) + [helices, avg_helix_length, fraction_paired]

    except Exception as e:
        logger.error(f"Error calculating features for sequence: {seq}. Error: {str(e)}")
        print_exc()
        return None

# Mateo Carvajal

def visualize_features(X: pd.DataFrame):
    try:
        logging.info("Visualizing feature distributions and correlations...")

        # Exclude one-hot encoded features (columns starting with 'OneHot_')
        features_to_plot = ["MFE", "Avg_BP_Prob", "Ensemble_Energy", "Helices", "Avg_Helix_Length", "Fraction_Paired"]

        print(features_to_plot)
        distribution_plots = []

        # Plot distributions for each feature
        for feature in features_to_plot:

            # Assuming X is your DataFrame and feature is the column you want to plot
            fig = px.histogram(
                X,
                x=feature,
                nbins=30,
                marginal="box",
                title=f'Distribution of {feature}',
                template="plotly_dark",
                color_discrete_sequence=["yellow"],
                opacity=0.8
            )

            # Customize the layout for better aesthetics, reduce dimensions, and center the plot
            fig.update_layout(
                title_font=dict(size=24, color='white'),
                xaxis=dict(title=feature, title_font=dict(size=18, color='white')),
                yaxis=dict(title='Count', title_font=dict(size=18, color='white')),
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white'),
                bargap=0.1,
                width=600,
                height=500,
                margin=dict(l=50, r=50, b=50, t=80, autoexpand=True),

            )
                # Customize the box plot (marginal)
            fig.update_traces(
                    marker=dict(line=dict(width=2, color='yellow')),
                    selector=dict(type='histogram')
                )


            distribution_plots.append(fig)

        # Compute correlation matrix
        corr_matrix = X[features_to_plot].corr()

        # Generate heatmap using Plotly
        heatmap_fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu',
            zmin=-1, zmax=1,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}"
        ))
        heatmap_fig.update_layout(title="Feature Correlation Matrix", template="plotly_dark")

        logging.info("Feature plots and correlation matrix prepared successfully.")
        return {name:plot for name,plot in zip(features_to_plot+['Feature Correlation Matrix'], distribution_plots + [heatmap_fig])}

    except Exception as e:
        logging.error(f"Error during feature visualization: {str(e)}")
        print_exc()
        return None


# Function to predict efficacy scores for k-mers
def predict_efficacy_scores(sequence, model_path='Backend/stacking_model.pkl'):
    logger.info(f"Input sequence provided")
    try:
        # Generate k-mers
        kmers = generate_kmers(sequence)
        logger.info(f"Generated {len(kmers)} k-mers ending with AG, GG, or GA.")

        if not kmers:
            logger.warning("No valid k-mers found.")
            return

        # Calculate features for each k-mer
        features = [calculate_features(kmer) for kmer in kmers]

        # Check if any feature calculation failed
        if None in features:
            logger.error("Feature calculation failed for one or more k-mers. Exiting.")
            return

        # Convert features to a DataFrame

        feature_names = ['MFE', 'Avg_BP_Prob', 'Ensemble_Energy'] + \
                        [f'OneHot_{i}' for i in range(92)] + \
                        ['Helices', 'Avg_Helix_Length', 'Fraction_Paired']
        X = pd.DataFrame(features, columns=feature_names)
        logger.info(f"Feature matrix created. Shape: {X.shape}")

        # Load the saved model
        logger.info("Loading the saved model...")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info("Model loaded successfully.")

        # Predict efficacy scores
        logger.info("Predicting efficacy scores...")
        predictions = model.predict(X)

        # Create a DataFrame with k-mers and their predicted efficacy scores
        X['k-mer'] = kmers
        results = pd.DataFrame({
            'k-mer': kmers,
            'Predicted_Efficacy': predictions
        })

        # Sort the results in descending order by Predicted_Efficacy
        results_sorted = results.sort_values(by='Predicted_Efficacy', ascending=False,ignore_index=True)
        results_sorted = pd.merge(results_sorted,X,on='k-mer',how='inner')
        return results_sorted
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        print_exc()
        return None
