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


# Data Quality Analysis
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

# Bias & Fairness
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


# Privacy Risks
Because credit application datasets contain sensitive personal information, we evaluated the dataset from a privacy and data protection perspective. The objective of this analysis was to identify personally identifiable information (PII) present in the dataset and demonstrate how privacy-preserving techniques such as pseudonymization can reduce the risk of exposing sensitive data while still allowing analytical use.

## Identification of Personal Data
The dataset contains several attributes that qualify as personally identifiable information (PII) because they can directly identify applicants or allow individuals to be re-identified when combined with other variables.
The following PII fields were identified in the dataset:
- full_name - applicant´s full legal name
- email - personal email address
- ssn - social security number
- ip_address - ip addressed used during application
- date_of_birth - applicant date of birth
- zip_code - geographic location

Some of these fields, particularly SSN, email, and IP address, are considered highly sensitive identifiers and require strong protection mechanisms under data protection regulations.

## Privacy Risks in the Raw Dataset
In the original dataset, these identifiers are stored in plain text format, which introduces several governance and security risks:
- Direct identifiers such as names and SSNs are accessible in raw form
- Personal identifiers can be used to re-identify individuals
- No protection mechanisms (e.g., hashing or encryption) are applied
- The dataset includes more personal information than strictly necessary for analysis

## Pseudonymization Demonstration
To demonstrate how privacy risks can be reduced, we applied pseudonymization techniques to sensitive identifiers.
Specifically, the Social Security Number (SSN) field was transformed using a cryptographic hashing function. Hashing converts the original identifier into a fixed-length encoded value that cannot easily be reversed.
Example transformation:
- XXX-XX-1234 - a8f5f167f44f4964e6c998dee827110c

After hashing, the identifier can no longer directly reveal the original SSN while still allowing consistent linking of records if needed for analysis.
This approach reduces the risk of exposing sensitive personal identifiers while preserving analytical utility.

## GDPR Implications
The presence of multiple direct identifiers in the dataset highlights several areas where stronger governance controls are required to align with GDPR principles.
- Data minimization - Excessive personal identifiers included in analytical dataset
- Security of processing - Sensitive identifiers stored without protection
- Privacy by design - No pseudonymization applied in raw dataset

Implementing pseudonymization techniques, such as the hashing approach demonstrated in this analysis, can significantly improve compliance with GDPR privacy-by-design requirements.

## Governance Implications
From a governance perspective, organizations handling credit application data should implement additional privacy controls, including:
- pseudonymization of sensitive identifiers before analysis
- encryption of personal data during storage and transmission
- clear data retention policies
- strict access controls for sensitive personal information

These controls help ensure that financial institutions process personal data in a manner that protects individuals while still enabling responsible analytical use.
