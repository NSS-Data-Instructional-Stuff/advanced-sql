## Optimizing Inefficient Queries in BigQuery

The goal of these exercises is to rewrite the given query to be more efficient. Bytes processed/billed and Slot milliseconds are prime indicators of efficiency in BigQuery.

1. For conditions recorded in the year 2010, how many distinct patients received each condition? Show the condition concept ID and the patient count.

SELECT *,
  COUNT(DISTINCT person_id) AS patient_count
FROM `bigquery-public-data.cms_synthetic_patient_data_omop.condition_occurrence`
WHERE EXTRACT(YEAR FROM condition_start_date) = 2010
GROUP BY ALL;

-----------------------------------

2. What is the total count of conditions recorded for each patient whose gender is 'MALE' and who was born before 1950?
(Hint: you may or may not need the columns specifically included in the main query)

WITH condition AS (
  SELECT *
  FROM `bigquery-public-data.cms_synthetic_patient_data_omop.condition_occurrence`
),

patient AS (
  SELECT *
  FROM `bigquery-public-data.cms_synthetic_patient_data_omop.person`
)

SELECT
  t2.person_id,
  COUNT(t1.condition_occurrence_id) AS total_conditions,
  condition_start_date,
  condition_end_date,
  t2.provider_id
FROM condition AS t1
INNER JOIN patient AS t2
  ON t1.person_id = t2.person_id
WHERE
  t2.gender_concept_id = 8507 -- Concept ID for 'MALE'
  AND t2.year_of_birth < 1950
GROUP BY ALL;

---------------------------

3. In the entire dataset, compare the number of times Diabetes (Concept ID: 201820) was recorded versus the number of times Atrial Fibrillation (Concept ID: 313217) was recorded, grouped by the condition's source value text.

SELECT t1.condition_source_value,
  COUNT(CASE WHEN t1.condition_concept_id = 201820 THEN 1 END) AS diabetes_count,
  COUNT(CASE WHEN t2.condition_concept_id = 313217 THEN 1 END) AS afib_count
FROM `bigquery-public-data.cms_synthetic_patient_data_omop.condition_occurrence` AS t1
LEFT JOIN `bigquery-public-data.cms_synthetic_patient_data_omop.condition_occurrence` AS t2
  ON t1.condition_source_value = t2.condition_source_value
WHERE t1.condition_concept_id IN (201820, 313217)
GROUP BY 1;

----------------------------

4. Find all unique condition source values where the text contains a 3-digit number.

SELECT DISTINCT condition_source_value
FROM `bigquery-public-data.cms_synthetic_patient_data_omop.condition_occurrence`
WHERE REGEXP_CONTAINS(condition_source_value, r'[0-9]{3}')
  AND condition_start_date IS NOT NULL;

----------------------------

5. Find the person who was born the earliest (the oldest patient) in the dataset.

SELECT
  person_id,
  year_of_birth
FROM (
  SELECT
    person_id,
    year_of_birth,
    ROW_NUMBER() OVER (ORDER BY year_of_birth ASC) AS rn
  FROM `bigquery-public-data.cms_synthetic_patient_data_omop.person`
)
WHERE rn = 1;

---------------------------

6. List the person_id and year_of_birth for all male patients who are 65 or older as of 2010.

SELECT
  person_id,
  gender_concept_id,
  year_of_birth,
  race_concept_id,
  ethnicity_concept_id,
  location_id
FROM `bigquery-public-data.cms_synthetic_patient_data_omop.person`
WHERE gender_concept_id = 8507 -- Concept ID for 'MALE'
  AND (2010 - year_of_birth) >= 65;

