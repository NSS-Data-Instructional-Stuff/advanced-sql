## Week 2, Part 2 Window Functions in BigQuery

This set of exercises is designed to give you more practice with window functions, as well as the QUALIFY function in BigQuery. You will be using the bigquery-public-data.cms_synthetic_patient_data_omop dataset.

------------------------------
### Question 1
Use the condition_occurrence table to return each patient's earliest recorded condition. Include person_id, condition_occurrence_id, condition_concept_id, and condition_start_date in the results. Do not use a CTE or subquery in your answer.

### Question 2
Find the most recent exposure for each unique combination of person_id and drug_concept_id (hint, you will want to order by drug_exposure_start_date descending). Return person_id, drug_concept_id, drug_exposure_start_date, days_supply, and quantity. Consider using a CTE to pre-filter the data to include only valid concept IDs (non-zero).

### Question 3
Using the condition_occurrence table, produce a running total of how many distinct condition records each patient has accumulated over time ordered by person_id and condition_start_date.

For each row, show the cumulative count of condition records up to and including that date using a running SUM window with ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. Include person_id, condition_concept_id, condition_start_date, and running_condition_count.

### Question 4
Find the top 3 most frequent conditions per gender. You'll want to join condition_occurrence with person to bring in gender_concept_id.
(Hint: join the concept table as well on condition_concept_id to get the human-readable concept name. A reasonable approach would be to use a CTE to build a table with the aggregated counts.)

### Question 5
The drug_exposure table sometimes has multiple records for the same patient and drug on the same start date. Write a query that deduplicates these, keeping only the record with the highest days_supply per person_id/drug_concept_id/drug_exposure_start_date combination. (Hint: you'll use QUALIFY for this but no CTE or subquery.)

### Question 6 (challenge)
Use the condition_occurrence table to aggregate the total number of condition records per year. Calculate absolute year-over-year change and year-over-year percent change by condition_concept_id and order the final output by absolute year-over-year change descending. (Hint: use a CTE for the initial aggregation. Your main query will involve the LAG window function. Make sure to only include condition concepts in the final output where the data exists for at least 2 years.)

### Question 7 (challenge)
Use the drug_era table to calculate the medication burden per patient and group them into quartiles. The number of records in the drug_era table can be considered a proxy for medication burden over their history. After calculating the medication burden per patient, assign each patient to a quartile (1=fewest to 4=most). Calculate the percent rank within each quartile for each patient to show where they sit in the distribution. Also include a CASE statement to give human-readable names to the quartiles which is important for reporting. (Hint: look for the BigQuery documentation on the NTILE, PERCENT_RANK, and CASE functions.)