import RNA
import pandas as pd
import numpy as np
import pickle
import logging
import plotly.express as px
import plotly.graph_objects as go
from traceback import print_exc


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Working_part/kmer_prediction.log'),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

# Function to calculate features for a single RNA sequence
def calculate_features(seq):
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

        # 3. Thermodynamic properties (using ensemble free energy as an example)
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

# Function to generate all k-mers of length 23 ending with AG, GG, or GA
def generate_kmers(sequence, k=23):
    kmers = []
    suffixes = ['AG', 'GG', 'GA']
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        if kmer[-2:] in suffixes:
            kmers.append(kmer)
    return kmers

