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
 
# Key Findings


# Data Quality Analysis:
The original dataset consisted of 502 credit applications stored in a nested JSON structure. Each record contained multiple nested objects, including applicant information, financial data, spending behavior, and loan decision outcomes. Because of this structure, the dataset first required transformation into a flat tabular format to allow analysis.

## Data Transformation
The dataset was flattened by extracting nested attributes into structured columns. Key transformations included:
- Extracting applicant attributes (e.g., gender, ZIP code, date of birth)
- Extracting financial variables (income, credit history, debt-to-income ratio)
- Transforming the spending_behavior array into structured numerical features
- Isolating the loan decision variable as the target outcome

This process produced a structured dataset suitable for analysis and further governance evaluation.

## Missing Data Analysis
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

## Data Cleaning Actions
To prepare the dataset for downstream analysis, the following cleaning steps were performed:
- Flattened nested JSON records into tabular format
- Removed columns with extreme missing values
- Structured spending behavior into usable features
- Standardized the dataset for statistical analysis

## Final Analytical Dataset
After cleaning and transformation, the dataset consisted of:
- 502 observations
- structured applicant, financial, behavioral, and decision variables
- a binary loan approval outcome

The distribution of the target variable was:
- 292 - Approved
- 210 - Rejected

This relatively balanced distribution makes the dataset suitable for fairness and bias analysis, which will be explored in the next phase of the project.
From a governance perspective, the high level of missing information in several fields indicates weaknesses in data collection and validation processes. Implementing stronger data validation controls during data ingestion would help ensure more reliable credit decision data in the future.

# Bias & Fairness:
Following the data cleaning process, we analyzed whether NovaCred’s historical lending decisions exhibit potential bias across demographic groups. Since automated credit decision systems can unintentionally produce discriminatory outcomes, fairness analysis is essential for responsible governance and regulatory compliance.

## Gender Approval Rate Comparison
We first examined loan approval rates across gender groups to determine whether one group systematically received more favorable lending outcomes.
The approval rates were calculated as the proportion of approved applications within each gender category.
- male - 66%
- female - 51%

This comparison provides an initial indication of whether lending decisions differ significantly across groups.

## Disparate Impact Ratio
To formally assess fairness, we calculated the Disparate Impact (DI) Ratio, a commonly used fairness metric in algorithmic decision systems.
The metric is defined as:
*DI = Approval Rate (Unprivileged Group(Male)) / Approval Rate (Privileged Group(Female))*
According to the four-fifths rule, a DI value below 0.8 may indicate potential disparate impact or discrimination.
- DI = 0.7698

This falls below the 0.80 four-fifths threshold, so the 80% rule is triggered, indicating potential adverse impact against the female group in the observed decision outcomes.

## Statistical Association Test
To complement the DI metric, we tested whether loan approval outcomes are statistically associated with gender using a chi-square test of independence.
The test result shows:
- χ²(1) = 11.12, p = 0.000856

Because the p-value is below conventional significance thresholds, we reject the null hypothesis that approval decisions are independent of gender. This indicates that approval outcomes differ across gender groups in the observed data.
To measure the strength of this relationship, we computed Cramer’s V, which provides an effect size for categorical association.
- Cramer´s V = 0.149

This value indicates a weak-to-moderate association between gender and loan approval outcomes.

## Proxy Discrimination Analysis
Even if protected attributes are not directly used in lending decisions, other variables may act as proxies, indirectly reproducing demographic patterns.
We evaluated candidate proxy variables using a two-step approach:
- Test whether a variable is associated with gender
- Test whether the same variable is associated with approval outcomes

A variable is considered a potential proxy risk only if both relationships exist.
Our analysis identified ZIP code as strongly associated with gender:
- χ² = 393.73, p < 0.001

However, ZIP code did not show evidence of association with loan approval outcomes, suggesting that it does not function as an active proxy for gender in the current dataset.

## Interpretation
Overall, the fairness analysis indicates that approval outcomes are statistically associated with gender, although the observed effect size is relatively modest. These findings highlight the importance of ongoing fairness monitoring and governance oversight to ensure that automated credit decision systems operate equitably.


Privacy Risks:
-
-
-

