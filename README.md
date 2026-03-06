# dego-project-team6
DEGO Course Project - Team 6


## Team Members:
- Leonor Oliveira
- António Grincho
- Lu Gan
- Pietro Franchi




## Project Description
Credit scoring bias analysis for DEGO course.


## Structure
- ‘data /‘ - Dataset files
- ‘notebooks /‘ - Jupyter analysis notebooks
- ‘src /‘ - Python source code
- ‘reports /‘ - Final deliverables


# Executive Summary
NovaCred, a fintech company that uses automated systems to evaluate credit applications, recently received a regulatory inquiry regarding potential discrimination in its lending decisions. Our team was tasked with conducting a governance audit of the credit application dataset to evaluate data quality, algorithmic bias, and privacy compliance.


The analysis was structured around three core governance pillars:


1. Data Quality Assessment
2. Bias & Fairness Evaluation
3. Privacy and Regulatory Compliance


The goal of this audit is to identify operational risks in NovaCred’s credit decision pipeline and propose governance controls aligned with GDPR and the EU AI Act.
 
 ## Key Findings


## Data Quality Analysis:
The original dataset consisted of 502 credit applications stored in a nested JSON structure. Each record contained multiple nested objects, including applicant information, financial data, spending behavior, and loan decision outcomes. Because of this structure, the dataset first required transformation into a flat tabular format to allow analysis.

# Data Transformation
The dataset was flattened by extracting nested attributes into structured columns. Key transformations included:
- Extracting applicant attributes (e.g., gender, ZIP code, date of birth)
- Extracting financial variables (income, credit history, debt-to-income ratio)
- Transforming the spending_behavior array into structured numerical features
- Isolating the loan decision variable as the target outcome

This process produced a structured dataset suitable for analysis and further governance evaluation.

# Missing Data Analysis
A data quality audit revealed several fields with extremely high levels of missing data. The most significant issues were:

- notes 99.6% missing
- annual salary 99% missing
- loan purpose 90% missing
- processing timestamp 87.6% missing

Because the *notes* and *annual_salary* variables contained almost no usable data, they were removed from the dataset before further analysis.
A small number of missing values were also observed in the following fields:

- Social Security Number (SSN)
- Annual income
- IP address

These occurred in approximately 1% of records and were retained in the dataset to support later privacy and governance analysis.

# Data Cleaning Actions
To prepare the dataset for downstream analysis, the following cleaning steps were performed:

- Flattened nested JSON records into tabular format
- Removed columns with extreme missing values
- Structured spending behavior into usable features
- Standardized the dataset for statistical analysis

# Final Analytical Dataset
After cleaning and transformation, the dataset consisted of:
- 502 observations
- structured applicant, financial, behavioral, and decision variables
- a binary loan approval outcome

The distribution of the target variable was:

- 292 - Approved
- 210 - Rejected

This relatively balanced distribution makes the dataset suitable for fairness and bias analysis, which will be explored in the next phase of the project.
From a governance perspective, the high level of missing information in several fields indicates weaknesses in data collection and validation processes. Implementing stronger data validation controls during data ingestion would help ensure more reliable credit decision data in the future.

Bias & Fairness:
-
-
-


Privacy Risks:
-
-
-

