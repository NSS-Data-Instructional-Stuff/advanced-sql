## Week 5, Part 1: Introduction to BigQuery

This set of exercises is designed to get you oriented to using the BigQuery platform and the public datasets made available by Google.

Google has excellent documentation for BigQuery - you'll find an overview here and links to other sections of the documentation.
https://cloud.google.com/bigquery/docs

-----------------------------------
### Question 1
Calculate the total number of distinct providers who performed a procedure on a patient who has a documented diagnosis of Type 2 Diabetes Mellitus (condition_concept_id = 201826)

### Question 2
List the unique person_id values and race_source_value of patients who had Type 2 Diabetes Mellitus (condition_concept_id = 201826) documented in at least three separate condition_occurrence records in the year 2009.

### Question 3
Use a CTE to first calculate the average quantity of all drug exposures in the dataset. Then, use that average to count how many patients with Type 2 Diabetes Mellitus (condition_concept_id = 201826) received carbamazepine (drug_concept_id = 19074697) in a quantity greater than the overall average. (Hint: you can solve this with an intentional Cartesian join)

### Question 4
Rank the top five providers based on the total count of procedures (procedure_occurrence_id) they documented. (Hint: use DENSE_RANK() to assign the same rank to providers with the same procedure count.)

### Question 5
Find the unique person IDs of patients who had a Type 2 Diabetes Mellitus diagnosis (condition_concept_id = 201826) in 2008 AND a documented drug exposure record, BUT who have NO documented procedure occurrence records (at any time).

### Question 6
For each patient, calculate the number of days between their current Type 2 Diabetes Mellitus diagnosis date and the date of their previous T2DM diagnosis.