# CRISPR-Guide-RNA-Design-Tool

<p align="center">
 
<img src="circular_logo.png" align="center" width="300" height="300" >
</p>

## Description

Castor is a tool designed to simplify the gRNA design process in Clustered Regularly Interspaced Short Palindromic Repeats (CRISPR)-associated protein 9 (Cas9) projects. The platform identifies gRNA sequences from input FASTA files based on specified PAM patterns and ranks them by predicted performance using a pre-trained ML model. The outputs include **predicted efficacy scores** for guide RNAs (gRNAs), **annotated gRNA data with biological features** (e.g., GC content, entropy, Tm), and visualizations such as **efficacy score distributions**, feature correlations, and boxplots. The results are saved to a CSV file for further analysis, and detailed logs ensure reproducibility and debugging support.

----
## Functionalities

This Python-based pipeline is designed for CRISPR guide RNA (gRNA) analysis. Pandas and NumPy libraries were used for data handling, scikit-learn for preprocessing and predictions, and Matplotlib and Seaborn for visualization. It employs a machine learning model to predict gRNA efficacy based on sequence features such as GC content, entropy, and melting temperature (Tm). Secondary features like k-mer encoding are also included for comprehensive analysis.

## Data Sources and Processing
The input data consists of gRNA sequences extracted from FASTA files, processed with a PAM pattern matching ( "NGG") to identify target sequences. Sequences are enriched with biological features and normalized using scikit-learn's StandardScaler for uniformity. Pre-trained machine learning models, such as ensemble methods, predict the efficacy of each gRNA, with results formatted for downstream analysis.

## Data Storage and Structure
Pandas DataFrames store the gRNA data, incorporating features such as sequence length, GC content, entropy, and PAM presence. Results, including predicted efficacy scores, are saved as CSV files to ensure compatibility with external tools.

## User Interface and Accessibility
Streamlit was used to create a user-friendly interface for uploading FASTA files and viewing the predictions.It allow users to customize experimental parameters and download results.

## Statistical Analysis and Model Performance
The efficacy prediction relies on robust statistical techniques and machine learning models. Metrics such as regression accuracy and feature importance are computed to validate model performance across multiple datasets.

## Visualizations
Comprehensive visualizations using Matplotlib and Seaborn include:

Histograms for predicted efficacy score distributions.
Correlation heatmaps of biological features.
Boxplots for key metrics like GC content and sequence entropy.


----
## Installation and Usage
Users will be able to install the necessary libraries with a single command: include Streamlit, and machine learning packages such as scikit-learn. 

----
## Timeline
![An example schedule](timeline.png)
## Group Details
Example:
- Group name: CRISPR
- Group code: G18
- Group repository: https://github.com/bsa674/CRISPR-Guide-RNA-Design-Too
- Tutor responsible: Frederik Hennecke
- Group team leader: Samanta Bishal
- Group members:Agrawal Raghvendra, Aslan Zeynep, Carvajal Mateo, Alarcón Pablo

## Acknowlegdments

- Streamlit - Web application framework for creating interactive data app
- Documentation: https://docs.streamlit.io/
- Pandas - Data manipulation and analysis library.
- Documentation: https://pandas.pydata.org/
- Matplotlib and Seaborn - Libraries for data visualization in Python.
- Matplotlib: https://matplotlib.org/
- Seaborn: https://seaborn.pydata.org/
- scikit-learn - Machine learning library for Python.
- Documentation: https://scikit-learn.org/
- XGBoost - Scalable machine learning library for gradient boosting.
Documentation: https://xgboost.readthedocs.io/

## Data Repositories & Resources
1) ENCODE (Encyclopedia of DNA Elements)
Website: https://www.encodeproject.org/
2) CRISPRBase - Repository for CRISPR research data.
Website: https://www.crisprbase.com/
3) GEO (Gene Expression Omnibus) - Database for functional genomics data.
Website: https://www.ncbi.nlm.nih.gov/geo/
4) SRA (Sequence Read Archive) - Repository for raw sequencing data.
Website: https://www.ncbi.nlm.nih.gov/sra
5) Figshare - General-purpose repository for scientific datasets.
Website: https://figshare.com/


## Relevant Publications
1) Chen, Y., & Wang, X. (2022). Evaluation of efficiency prediction algorithms and development of ensemble model for CRISPR/Cas9 gRNA selection. Bioinformatics, 38(23), 5175-5181.
DOI: https://doi.org/10.1093/bioinformatics/btac681
2) Doudna, J.A., & Charpentier, E. (2014). The new frontier of genome engineering with CRISPR-Cas9. Science, 346(6213), 1258096.
DOI: https://doi.org/10.1126/science.1258096
3) Doench, J.G., et al. (2016). Optimized sgRNA design to maximize activity and minimize off-target effects of CRISPR-Cas9. Nature Biotechnology, 34, 184-191.
DOI: https://doi.org/10.1038/nbt.3437
4) Konstantakos, V., et al. (2022). CRISPR-Cas9 gRNA efficiency prediction: an overview of predictive tools and the role of deep learning. Nucleic Acids Research, 50, 3616-3637.
DOI: https://doi.org/10.1093/nar/gkab1114
5) Kim, H.K., et al. (2019). SpCas9 activity prediction by DeepSpCas9, a deep learning-based model with high generalization performance. Science Advances, 5(11), eaax9249.
DOI: https://doi.org/10.1126/sciadv.aax9249
