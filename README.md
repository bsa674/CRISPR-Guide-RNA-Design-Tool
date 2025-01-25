# CRISPR-Guide-RNA-Design-Tool

![CASTOR](banner_logo.png)

## Description

Castor is a tool designed to simplify the gRNA design process in Clustered Regularly Interspaced Short Palindromic Repeats (CRISPR)-associated protein 9 (Cas9) projects. The platform comprises two modules: one dedicated to the design of single guide RNAs (sgRNAs) and another focused on assessing their efficiency using ML models. 

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

Here, you should provide a group name you want to be referred to as, as well as the names (and optionally contact info) of all group members.
Additionally, define a group leader, i.e. one person in your group that is the primary contact if tutors want to communicate with your group.
Also mention here which tutor is assigned to your project.

Example:
- Group name: 
- Group code: 
- Group repository: 
- Tutor responsible:  
- Group team leader: 
- Group members:

Include also the (detailed) contribution of each group member to the development of the project.

Example:
**Member A**: Developed the data structure of the project. Helped _Member B_ on the web interface and user management. Refactoring on components X, Y, and Z. Responsible for the unit tests in P ant T.

----
## Acknowlegdments

Here, you can (and should) mention all libraries you used, data sources, as well as other credits such as inspirations for your projects, papers that helped with your methodology or similar things.

If you want, you can create subsections for all of these, or just create bullet-points for it. If possible, provide a link to the original source(s).
