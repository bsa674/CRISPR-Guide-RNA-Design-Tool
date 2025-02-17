# CRISPR-Guide-RNA-Design-Tool

<p align="center">
 
<img src="circular_logo.png" align="center" width="300" height="300" >
</p>

## Description

Castor is an innovative platform designed to simplify and optimize the process of guide RNA (gRNA) design for CRISPR-Cas9 genome editing projects. By integrating advanced machine learning (ML) algorithms and bioinformatics tools, Castor automates the identification of gRNA sequences from input FASTA files, ensuring compatibility with user-specified Protospacer Adjacent Motif (PAM) patterns. The platform ranks these gRNA sequences based on predicted efficacy using a pre-trained ML model, providing researchers with reliable performance scores to guide their selection. 

In addition to efficacy predictions, Castor annotates each gRNA with critical biological features, such as Minimized Free Energy (MFE), Average Base-Pairing Probability, and Ensemble Energy, offering deeper insights into the molecular characteristics of the designed gRNAs. To further enhance usability, the platform generates comprehensive visualizations, including feature distribution plots and correlation matrices, enabling researchers to explore and interpret the data effectively. Castor also prioritizes reproducibility and transparency by maintaining detailed logs throughout the process, ensuring that every step of the gRNA design process is traceable and debuggable. 

With its user-friendly interface, robust analytical capabilities, and emphasis on reproducibility, Castor is an essential tool for researchers seeking to streamline and enhance the efficiency of their CRISPR-Cas9 genome editing projects.

----
## Functionalities

This Python-based pipeline is designed for **CRISPR guide RNA (gRNA) analysis**, combining bioinformatics and machine learning to predict gRNA efficacy. It utilizes **Pandas** and **NumPy** for data handling, **ViennaRNA** for RNA secondary structure prediction, and **Plotly** for interactive visualizations. A **stacking ensemble model**, integrating **Random Forest** and **XGBoost**, predicts gRNA efficacy based on extracted features such as minimum free energy (MFE), base-pairing probabilities, and helical properties. The pipeline includes a **Streamlit-based web application** for user-friendly interaction, enabling users to upload FASTA files, customize parameters, view predictions, and download results and visualizations. Designed for both computational and experimental researchers, this tool provides a comprehensive solution for gRNA analysis and efficacy prediction.

## Data Sources and Processing

#### Model Creation
To develop the model, we utilized a curated dataset sourced from various databases and publications. The dataset is stored in a CSV file containing two primary columns: 
- **gRNA sequences**: The guide RNA sequences.
- **Efficacy scores**: The corresponding efficacy scores for each gRNA sequence.

The gRNA sequences were enriched with biological features and encoded using one-hot encoding to create a comprehensive feature matrix. This matrix served as the input for our machine learning model.

We employed a **Stacking-Ensemble regressor model**, which combines the strengths of **Random Forest** and **XGBoost** algorithms, to predict the efficacy scores based on the input features.

#### User Input Processing
For user input, the model accepts a single FASTA sequence. The sequence is processed as follows:
1. **Sequence Breakdown**: The input sequence is divided into 23-mer subsequences, each ending with a **PAM sequence**.
2. **Feature Extraction**: The same biological features used during model training are calculated for each 23-mer subsequence.
3. **Prediction**: The pre-trained Stacking-Ensemble regressor model is then used to predict the efficacy scores for each subsequence.

This pipeline ensures accurate and efficient prediction of gRNA efficacy based on user-provided sequences.

## Data Storage and Structure

#### Training Data
The original dataset used for training the model is stored as a CSV file in the local directory. The file contains two columns:
- **gRNA**: The guide RNA sequences.
- **Efficacy Scores**: The corresponding efficacy scores for each gRNA.

#### Prediction Results
The results generated after running predictions are also saved locally on the system for easy access and further analysis.

#### Stacking Ensemble Model
The trained stacking ensemble model is saved as a **pickle file** (`stacking_model.pkl`) in the local directory. This allows for easy loading and reuse of the model for future predictions without retraining.

#### User Account Credentials
User account credentials are securely stored on a Firebase server. All sensitive information is encrypted to ensure data privacy and security.


## User Interface and Accessibility

A **Streamlit**-based web application has been developed to provide a user-friendly and interactive interface for CRISPR-Cas prediction. The application includes the following features:

#### User Authentication
- **Login**: Users can securely log in to access their accounts and projects.
- **Create Account**: New users can easily create an account to start using the application.
- **Forgot Password**: Users can reset their password in case they forget it.
- **Forgot Username**: Users can retrieve their username if needed.

#### Project Management
- **Create Projects**: Users can create and manage multiple projects to organize their data and predictions efficiently.

#### Data Upload and Customization
- **Upload FASTA Files**: Users can upload their FASTA files containing gRNA sequences for analysis.

#### Predictions and Visualizations
- **View Predictions**: Users can view the predicted efficacy scores for their uploaded sequences.
- **Download Predictions**: Users can download the prediction results in a CSV format for further analysis.
- **Download Visualizations**: All visualizations, including the top 10 k-mers, feature distribution plots, and correlation matrix, are available for download.

#### Accessibility
Our application is designed to be user-friendly and accessible to a wide range of users, including both computational and experimental researchers. Whether you're a seasoned developer or new to data analysis, the application ensures a seamless experience for users with varying levels of technical expertise.

Web-Based Interface
The application is built using Streamlit, a powerful framework for creating interactive web applications. This allows users to access the platform directly from their web browsers without the need for complex installations or setups.

Key Features:
Login/Signup: Users can easily create an account or log in to access personalized features and save their work.

Task Execution: Perform a variety of tasks directly through the intuitive interface.

Visualization: View and interact with results through dynamic visualizations, making it easier to interpret data and draw insights.


## Statistical Analysis and Model Performance

A **Stacking Ensemble Model** was developed using **Random Forest** and **XGBoost Regressors** as base models. The performance of the model was evaluated using the following metrics:

- **R² Score (Coefficient of Determination)**: Measures the proportion of variance in the dependent variable that is predictable from the independent variables.
- **Mean Squared Error (MSE)**: Represents the average squared difference between the actual and predicted values.
- **Mean Absolute Error (MAE)**: Measures the average absolute difference between the actual and predicted values.

Additionally, **Actual vs Predicted Efficacy Plots** were generated to visually analyze the model's performance and the alignment between predicted and actual efficacy scores.

These metrics and visualizations provide a comprehensive understanding of the model's accuracy and effectiveness in predicting gRNA efficacy.

## Visualizations

#### Top 10 k-mers
The **top 10 k-mers** with the highest efficacy scores were identified and visualized. These k-mers represent the most effective sequences based on the user-provided data for CRISPR-Cas prediction. This visualization helps users understand which k-mers are likely to perform best in their experiments.

#### Feature Distribution Plots
Interactive **feature distribution plots** were generated using **Plotly**. These include histograms for all features, allowing users to explore the distribution of each feature in the dataset. The interactive nature of the plots enables users to zoom, hover, and analyze the data in detail.

#### Feature Correlation Matrix
A **feature correlation matrix** was created to visualize the relationships between different features in the dataset. This helps in identifying potential multicollinearity and understanding how features interact with each other.

#### Downloadable Visualizations
All visualizations, including the top 10 k-mers, feature distribution plots, and correlation matrix, are available for users to download and save to their local systems for further analysis or reporting.


### This pipeline provides an efficient and interpretable framework for gRNA efficacy prediction and CRISPR guide design.

----
## Installation and Usage

To set up and run this pipeline, follow these steps:  

1. **Clone the GitHub Repository**:  
   ```bash
   git clone <repository_url>
   cd <repository_directory>
    ```
2. **Install Dependencies**:
The required dependencies are listed in the provided dependencies file. Install them using:
 ```bash
  pip install -r requirements.txt
 ```
3. **Run the script**
   Open a python terminal in the base directory and write:
   ```bash
   `streamlit run ./main.py
   ```
   Note: Unzip the pkl model file (`stacking_model.zip`) in the directory `Backend\stacking_model.pkl` to use the pre-trained model for the predictions for the user.
         Alternatively, you can login as a admin and create the model file.
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
- Group members and contribution:

**Samanta Bishal**: Project Lead, organization, machine Learning development, and database curation
**Mateo Carvajal**: Assisted in searching and compiling the database for model training, code for the model's usage and visualization.
**Zeynep Aslan**: Helped in database curation and  developed the code for model usage, including prediction and visualization tools.
**Pablo Alarcón**: User-friendly web interface, user account management, including authentication and user profile systems
**Raghvendra Agrawal**: User-friendly web interface, helped implemented statistical analysis and dynamic visualization features for the web interface.

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
