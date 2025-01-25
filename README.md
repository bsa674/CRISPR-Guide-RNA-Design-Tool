# CRISPR-Guide-RNA-Design-Tool

![CASTOR](circular_logo.png)

## Description

Castor is a tool designed to simplify the gRNA design process in Clustered Regularly Interspaced Short Palindromic Repeats (CRISPR)-associated protein 9 (Cas9) projects. The platform identifies gRNA sequences from input FASTA files based on specified PAM patterns and ranks them by predicted performance using a pre-trained ML model. The outputs include **predicted efficacy scores** for guide RNAs (gRNAs), **annotated gRNA data with biological features** (e.g., GC content, entropy, Tm), and visualizations such as **efficacy score distributions**, feature correlations, and boxplots. IThe results are saved to a CSV file for further analysis, and detailed logs ensure reproducibility and debugging support.

----
## Functionalities

 Python libraries such as Pandas and NumPy for data manipulation, scikit-learn for data normalization, and RNAfold for secondary structure prediction. Prediction algorithms with machine learning models like scikit-learn, XGBoost and RandomForest. After model training, for the visualization with Matplotlib and Seaborn. A lightweight web interface is developed using Flask or Streamlit, enabling users to input custom gRNA sequences and experimental conditions, receiving real-time predictions on efficiency scores and feature importance.


### Data Sources and Retrieval

Resources like ENCODE, CRISPRBase, and CRISPRBench are ideal, as they offer curated datasets with gRNA sequences and associated efficiency labels.To retrieve the most relevant datasets, we used targeted search terms like “CRISPR gRNA efficiency,” “CRISPR/Cas9 cleavage data,” and “guide RNA performance”. Essential preprocessing steps will involve converting the data to a standard format, normalizing features, handling any missing values, and ensuring consistent annotation across datasets.

### Data Storage and Handling

 we used Python tools like Pandas to verify their completeness and structure.  we extracted sequence-based features like GC content, dinucleotide frequency, and potential off-target binding site.

### User Management
We implemented a secure encryption system using a discrete encryption key to verify user credentials. Each user account will maintain exclusive access to its own data, which will be securely stored and accessible at any time.
### Interface
The CRISPR gRNA prediction project will be developed as a web-based application using Python's Streamlit library. Users will start with a login page and dedicated results page will allow users to visualize and analyse gRNA efficiency scores, with results saved to their account for ongoing research. 

### Statistical Analysis
In the CRISPR gRNA prediction project, we focus on evaluating the performance and reliability of our ensemble model through a detailed statistical analysis.We calculated metrics for each baseline and ensemble model using Python libraries like scikit-learn, averaging results across multiple validation datasets to ensure robustness. 

### Visualizations

We used Python libraries like Matplotlib, Seaborn, and Plotly to create a comprehensive set of visual tools for showcasing our ensemble model's results. Plots will showed predicted versus actual efficiency scores, with regression lines indicating the model's fit quality.



----
## Installation and Usage
Users will be able to install the necessary libraries with a single command: include Streamlit, and machine learning packages such as scikit-learn. 

----
## Timeline

Give some outline as to what should be achieved at what time during project development.
You could also create a visual guide, such as this
![An example schedule](schedule.png)

to make sure all relevant aspects of developing an application are accounted for with sufficient time, and in sensible order.
This can also help you and the tutors to make sure the development does not go off the rails, and thus ensure a finished project at the deadline.

----
## Group Details
Example:
- Group name: CRISPR
- Group code: G18
- Group repository: https://github.com/bsa674/CRISPR-Guide-RNA-Design-Too
- Tutor responsible: Frederik Hennecke
- Group team leader: Samanta Bishal
- Group members:Agrawal Raghvendra, Aslan Zeynep, Carvajal Mateo, Alarcón Pablo

## Acknowlegdments

Streamlit - Web application framework for creating interactive data app
Documentation: https://docs.streamlit.io/
Pandas - Data manipulation and analysis library.
Documentation: https://pandas.pydata.org/
Matplotlib and Seaborn - Libraries for data visualization in Python.
Matplotlib: https://matplotlib.org/
Seaborn: https://seaborn.pydata.org/
scikit-learn - Machine learning library for Python.
Documentation: https://scikit-learn.org/
XGBoost - Scalable machine learning library for gradient boosting.
Documentation: https://xgboost.readthedocs.io/

## Data Repositories & Resources
1)ENCODE (Encyclopedia of DNA Elements)
Website: https://www.encodeproject.org/
2)CRISPRBase - Repository for CRISPR research data.
Website: https://www.crisprbase.com/
3)GEO (Gene Expression Omnibus) - Database for functional genomics data.
Website: https://www.ncbi.nlm.nih.gov/geo/
4)SRA (Sequence Read Archive) - Repository for raw sequencing data.
Website: https://www.ncbi.nlm.nih.gov/sra
5)Figshare - General-purpose repository for scientific datasets.
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
