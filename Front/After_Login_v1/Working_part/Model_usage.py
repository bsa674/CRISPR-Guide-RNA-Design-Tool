import logging
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns
from Bio import SeqIO
import re
from sklearn.preprocessing import StandardScaler
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go

# admin uploads the csv file and gets the plot,pkl file

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to add biological features
def add_biological_features(data):
    """Add biological features to the guide RNA data."""
    data['GC_content'] = data['gRNA_PAM'].apply(lambda x: (x.count('G') + x.count('C')) / len(x))
    data['seq_length'] = data['gRNA_PAM'].apply(len)
    data['Tm'] = data['gRNA_PAM'].apply(lambda x: 4 * (x.count('G') + x.count('C')) + 2 * (x.count('A') + x.count('T')))
    data['entropy'] = data['gRNA_PAM'].apply(lambda x: -sum(x.count(b) / len(x) * np.log2(x.count(b) / len(x)) for b in 'ACGT' if x.count(b) > 0))
    data['first_A'] = data['gRNA_PAM'].apply(lambda x: 1 if x[0] == 'A' else 0)
    data['first_C'] = data['gRNA_PAM'].apply(lambda x: 1 if x[0] == 'C' else 0)
    data['first_G'] = data['gRNA_PAM'].apply(lambda x: 1 if x[0] == 'G' else 0)
    data['first_T'] = data['gRNA_PAM'].apply(lambda x: 1 if x[0] == 'T' else 0)
    data['last_A'] = data['gRNA_PAM'].apply(lambda x: 1 if x[-1] == 'A' else 0)
    data['last_C'] = data['gRNA_PAM'].apply(lambda x: 1 if x[-1] == 'C' else 0)
    data['last_G'] = data['gRNA_PAM'].apply(lambda x: 1 if x[-1] == 'G' else 0)
    data['last_T'] = data['gRNA_PAM'].apply(lambda x: 1 if x[-1] == 'T' else 0)
    data['has_PAM'] = data['gRNA_PAM'].apply(lambda x: 1 if x[-3:] == 'NGG' else 0)
    return data

# Function to encode sequences
def encode_sequences(sequences, k=4):
    """Encode sgRNA sequences using k-mer counting."""
    import itertools
    kmers = [''.join(p) for p in itertools.product('ACGT', repeat=k)]
    kmer_counts = sequences.apply(lambda seq: [seq.count(kmer) for kmer in kmers])
    logger.info(f"Sequences encoded with {k}-mer counting.")
    return np.array(kmer_counts.tolist())

# Function to find guide RNAs and predict efficacy scores
def find_guides_with_pam(fasta_file, pam_pattern="NGG", model_path=None):
    if model_path is None:
        logger.error("No model file specified. Please provide the path to a trained model.")
        return pd.DataFrame()  # Return empty DataFrame if model path is not specified

    try:
        # Load the trained model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded successfully from {model_path}.")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return pd.DataFrame()  # Return empty DataFrame if model loading fails

    # Validate the FASTA file
    # if not os.path.isfile(fasta_file):
    #     logger.error(f"File {fasta_file} does not exist.")
    #     return pd.DataFrame()  # Return empty DataFrame if the file is not found

    logger.info(f"Processing file: {fasta_file}")

    try:
        guide_rnas = []
        # Process the FASTA file
        for record in SeqIO.parse(StringIO(fasta_file), "fasta"):
            sequence = str(record.seq).upper()

            for match in re.finditer(f"([ACGT]{{20}}){pam_pattern.replace('N', '[ACGT]')}", sequence):
                guide_rna = match.group()
                guide_rnas.append(guide_rna)

        logger.info(f"Found {len(guide_rnas)} guide RNA sequences with PAM regions in {fasta_file}.")

        if not guide_rnas:
            logger.warning(f"No guide RNA sequences with PAM regions found in {fasta_file}.")
            return pd.DataFrame()  # Return empty DataFrame if no guide RNAs are found

        # Create a DataFrame for the identified guide RNAs
        data = pd.DataFrame({'gRNA_PAM': guide_rnas})
        logger.info("Guide RNA sequences extracted and prepared for prediction.")

        # Add biological features
        data = add_biological_features(data)

        # Encode sequences and preprocess features
        X_seq = encode_sequences(data['gRNA_PAM'])
        X_features = data[['GC_content', 'seq_length', 'Tm', 'entropy', 'first_A', 'first_C', 'first_G', 'first_T',
                            'last_A', 'last_C', 'last_G', 'last_T', 'has_PAM']].values

        scaler = StandardScaler()
        X_features = scaler.fit_transform(X_features)
        X = np.hstack((X_seq, X_features))

        # Predict efficacy scores
        predictions = model.predict(X)
        data['predicted_efficacy'] = predictions

        logger.info("Efficacy scores predicted for the guide RNA sequences.")

        # Visualizations
        visualize_predictions(data)

        return data

    except Exception as e:
        logger.error(f"Error processing FASTA file {fasta_file}: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error

# Function to visualize the results
def visualize_predictions(data):
    """Visualize predicted efficacy scores and biological feature distributions for Streamlit using Plotly."""
    plots = []

    # 1. Distribution of Predicted Efficacy Scores
    hist_plot = px.histogram(
        data,
        x="predicted_efficacy",
        nbins=20,
        title="Distribution of Predicted Efficacy Scores",
        template="plotly_white",
    )
    hist_plot.update_layout(
        xaxis_title="Predicted Efficacy",
        yaxis_title="Frequency",
        font=dict(size=14)
    )
    plots.append(hist_plot)

    # 2. Correlation Heatmap of Biological Features
    features = data[['GC_content', 'seq_length', 'Tm', 'entropy', 'first_A', 'first_C', 'first_G', 'first_T',
                     'last_A', 'last_C', 'last_G', 'last_T', 'has_PAM']]
    correlation = features.corr()

    heatmap = go.Figure(
        data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.columns,
            colorscale="balance",
            colorbar=dict(title="Correlation"),
        )
    )
    heatmap.update_layout(
        title="Correlation Heatmap of Biological Features",
        template="plotly_white",
        font=dict(size=14),
    )
    plots.append(heatmap)

    # 3. Boxplot of GC Content, Tm, and Entropy
    box_plot = px.box(
        data,
        y=["GC_content", "Tm", "entropy"],
        title="Boxplot of GC Content, Tm, and Entropy",
        template="plotly_white",
    )
    box_plot.update_layout(
        yaxis_title="Values",
        font=dict(size=14),
    )
    plots.append(box_plot)

    return plots


# Example Usage
#if __name__ == "__main__":

def run_ML(sequence):
    print(os.getcwd())
#    fasta_file = "sequence.txt"  # Replace with your FASTA file path
    model_file = "D:\GAU\Courses\Sem 1\Python Programming for Data Science\Project\project_test_1\Working_part\Stacking Ensemble_model.pkl"  # Replace with your saved model file path
    print(os.path.exists(model_file))
    predicted_data = find_guides_with_pam(sequence, model_path=model_file)
    if not predicted_data.empty:
#        print(predicted_data.head())
#        predicted_data.to_csv("predicted_guide_rnas.csv", index=False)
        logger.info("Results saved to predicted_guide_rnas.csv.")
        return predicted_data

