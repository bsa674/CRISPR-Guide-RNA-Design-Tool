import pandas as pd
import numpy as np
import random
import logging
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, StackingRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
import itertools
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Step 1: Load the dataset
def load_data(filepath):
    """Load sgRNA dataset from a CSV file."""
    try:
        data = pd.read_csv(filepath)
        logger.info(f"Data loaded successfully from {filepath}.")
        return data
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

# Step 2: Encode sgRNA sequences with k-mer counting
def encode_sequences(sequences, k=4):
    """Encode sgRNA sequences using k-mer counting."""
    kmers = [''.join(p) for p in itertools.product('ACGT', repeat=k)]
    kmer_counts = sequences.apply(lambda seq: [seq.count(kmer) for kmer in kmers])
    logger.info(f"Sequences encoded with {k}-mer counting.")
    return np.array(kmer_counts.tolist())

# Step 3: Biological feature extraction
def position_nucleotide_frequency(sequence, position_range=5):
    """Calculate the frequency of each nucleotide in the first and last few positions."""
    first_position = sequence[:position_range]
    last_position = sequence[-position_range:]
    return {
        'first_A': first_position.count('A') / position_range,
        'first_C': first_position.count('C') / position_range,
        'first_G': first_position.count('G') / position_range,
        'first_T': first_position.count('T') / position_range,
        'last_A': last_position.count('A') / position_range,
        'last_C': last_position.count('C') / position_range,
        'last_G': last_position.count('G') / position_range,
        'last_T': last_position.count('T') / position_range
    }

def add_biological_features(data):
    """Add biological features like GC content, sequence length, melting temperature (Tm), 
       entropy, and nucleotide frequency at specific positions."""
    
    def calculate_entropy(sequence):
        """Calculate the Shannon entropy of a sequence."""
        nucleotide_counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'}
        total_bases = len(sequence)
        probabilities = [count / total_bases for count in nucleotide_counts.values()]
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        return entropy

    # GC content
    data['GC_content'] = data['gRNA_PAM'].apply(lambda x: (x.count('G') + x.count('C')) / len(x))
    
    # Sequence length
    data['seq_length'] = data['gRNA_PAM'].apply(len)
    
    # Melting temperature (Tm)
    data['Tm'] = data['gRNA_PAM'].apply(lambda x: 4 * (x.count('G') + x.count('C')) + 2 * (x.count('A') + x.count('T')))
    
    # Sequence entropy
    data['entropy'] = data['gRNA_PAM'].apply(calculate_entropy)
    
    # Position-specific nucleotide frequencies
    position_frequencies = data['gRNA_PAM'].apply(position_nucleotide_frequency)
    position_frequencies_df = pd.DataFrame(position_frequencies.tolist())
    data = pd.concat([data, position_frequencies_df], axis=1)

    # Presence of PAM sequence
    data['has_PAM'] = data['gRNA_PAM'].apply(lambda x: 'NGG' in x)

    logger.info("Biological features added: GC content, sequence length, Tm, entropy, position-specific frequencies, PAM presence.")
    return data

# Step 4: Generate synthetic data
def generate_synthetic_data(data, num_samples=500):
    """Generate synthetic sgRNA sequences by introducing random mutations."""
    synthetic_data = []
    for _ in range(num_samples):
        original_seq = random.choice(data['gRNA_PAM'].values)
        seq = list(original_seq)

        mutation_type = random.choice(['substitution', 'insertion', 'deletion'])
        position = random.randint(0, len(seq) - 1)

        if mutation_type == 'substitution':
            seq[position] = random.choice('ACGT')
        elif mutation_type == 'insertion':
            seq.insert(position, random.choice('ACGT'))
        elif mutation_type == 'deletion':
            seq.pop(position)

        seq = ''.join(seq)[:len(original_seq)].ljust(len(original_seq), 'N')
        synthetic_data.append(seq)

    synthetic_df = pd.DataFrame({'gRNA_PAM': synthetic_data})
    synthetic_df['efficacy'] = random.choices(data['efficacy'], k=num_samples)
    logger.info(f"Synthetic data with {num_samples} samples generated.")
    return synthetic_df

# Step 5: Preprocess the data
def preprocess_data(data):
    """Preprocess the dataset with feature engineering and scaling."""
    data = add_biological_features(data)
    sequences = data['gRNA_PAM']
    efficacy_scores = data['efficacy']

    # Encode sequences and scale features
    X_seq = encode_sequences(sequences)
    biological_feature_names = ['GC_content', 'seq_length', 'Tm', 'entropy', 'first_A', 'first_C', 
                                'first_G', 'first_T', 'last_A', 'last_C', 'last_G', 'last_T', 'has_PAM']
    X_features = data[biological_feature_names].values

    scaler = StandardScaler()
    X_features = scaler.fit_transform(X_features)

    # Combine sequence encoding and biological features
    X = np.hstack((X_seq, X_features))
    y = efficacy_scores.values

    # Combine feature names
    sequence_feature_names = [f'kmer_{i+1}' for i in range(X_seq.shape[1])]
    feature_names = sequence_feature_names + biological_feature_names

    logger.info("Data preprocessing completed.")
    return X, y, feature_names

# Step 6: Split data
def split_data(X, y, feature_names):
    """Split the data into training and testing sets."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logger.info("Data split into training and testing sets.")

    # Convert X_train to a DataFrame with feature names
    X_train_df = pd.DataFrame(X_train, columns=feature_names)

    # Save X_train as a CSV file
    X_train_df.to_csv('X_train.csv', index=False)
    logger.info("X_train data saved as 'X_train.csv'.")
    return X_train, X_test, y_train, y_test

# Step 7: Model training and evaluation
def train_and_evaluate_model(model, X_train, y_train, X_test, y_test, model_name):
    """Train and evaluate a model."""
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    logger.info(f"{model_name} - Mean Squared Error: {mse:.4f}, R-squared: {r2:.4f}")
    return model, mse, r2

# Step 8: Main pipeline
def main_pipeline(filepath):
    # Load data
    data = load_data(filepath)

    # Generate synthetic data and augment
    synthetic_data = generate_synthetic_data(data, num_samples=500)
    data = pd.concat([data, synthetic_data], ignore_index=True)

    # Preprocess data
    X, y, feature_names = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_data(X, y, feature_names)

    # Models to train
    models = {
        "XGBoost": XGBRegressor(objective='reg:squarederror', random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42),
        "Stacking Ensemble": StackingRegressor(
            estimators=[
                ('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
                ('xgb', XGBRegressor(objective='reg:squarederror', random_state=42)),
                ('gb', GradientBoostingRegressor(random_state=42))
            ],
            final_estimator=GradientBoostingRegressor(random_state=42)
        )
    }

    # Train and evaluate each model
    for model_name, model in models.items():
        train_and_evaluate_model(model, X_train, y_train, X_test, y_test, model_name)

    # Ask if the user wants to save the model
    save_model = input("Do you want to save the trained model? (yes/no): ").strip().lower()
    if save_model == "yes":
        model_choice = input("Which model would you like to save (XGBoost, Random Forest, Stacking Ensemble)? ").strip()
        if model_choice in models:
            with open(f'{model_choice}_model.pkl', 'wb') as f:
                pickle.dump(models[model_choice], f)
            logger.info(f"{model_choice} model saved as '{model_choice}_model.pkl'.")
    
    # Ask if the user wants to visualize the biological features
    visualize = input("Do you want to visualize the distribution of biological features? (yes/no): ").strip().lower()
    if visualize == "yes":
        plt.figure(figsize=(12, 8))
        sns.boxplot(data=data[['GC_content', 'seq_length', 'Tm', 'entropy']])
        plt.title("Biological Feature Distributions")
        plt.xticks(rotation=45)
        plt.show()

    logger.info("Pipeline execution completed.")

if __name__ == "__main__":
    main_pipeline('data_enc.csv')
