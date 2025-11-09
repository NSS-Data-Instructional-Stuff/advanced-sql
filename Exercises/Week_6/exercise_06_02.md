## Working with Denormalized Data in BigQuery

These exercises will use the INFORMATION_SCHEMA view which contains a record for all the queries you've run so far in your sandbox project. You do not need to include a project qualifier in the FROM clause, but you must include a region qualifier.

Example:
SELECT creation_time
FROM `region-us`.INFORMATION_SCHEMA.JOBS

Here is the documentation for this view (including the table schema and field definitions). There are also a number of example queries to show different ways to use the data for monitoring various aspects of individual BigQuery jobs as well as overall usage.
https://docs.cloud.google.com/bigquery/docs/information-schema-jobs

1. Analyze all jobs that failed (state='DONE' and error_result IS NOT NULL) in the last 14 days. Your task is to extract the individual reason string from every reported error and determine the top 5 most frequently occurring error reasons across all failed jobs. (Hint: the error_result field is a STRUCT and the errors sub-field is a repeated array. You'll want to use UNNEST in this query.)

2. For all successful (state='DONE' and error_result IS NULL) query jobs completed in the last 7 days, return the job ID, the total tebibytes billed, and a unique, aggregated list (an array) of all project IDs, dataset IDs, and table IDs referenced in the query. The information is contained in the referenced_tables field. This shows which jobs consumed the most resources and what tables the data is coming from as well as converting the usage unit to the unit used for billing. The INFORMATION_SCHEMA.JOBS view has a total_bytes_billed field, the conversion from bytes to tebibytes is 1024 to the 4th power.
(Hint: Look at array functions, particularly ARRAY_AGG. You'll also need to UNNEST the referenced_tables field.)

3. Identify the single, longest-running QUERY job (based on job duration) created in the last 7 days. Once identified, return its job ID, its total duration in seconds, and the elapsed milliseconds (elapsed_ms) of its first recorded timeline event (index 0) and the elapsed milliseconds of its last recorded timeline event.
(Hint: the timeline field contains snapshots of the query execution. You'll want to access the first array element and the last but remember that there is not a standard number of elements in the array so getting the last element will need to depend on the array length.)

---------------------------
The following two questions will use a version of the drug_exposure table we have used previously. To create the necessary table, run the following query and save the results as a view in your project.

SELECT person_id,
  drug_concept_id,
  MIN(drug_exposure_start_date) AS drug_exposure_start_date,
  -- Use TO_JSON() to serialize the array of structs into a single native JSON type.
  TO_JSON(
    ARRAY_AGG(
      STRUCT(
        drug_exposure_start_datetime,
        drug_exposure_end_datetime,
        verbatim_end_date,
        drug_type_concept_id,
        stop_reason,
        refills,
        quantity,
        days_supply,
        sig,
        route_concept_id,
        lot_number,
        provider_id,
        visit_occurrence_id,
        visit_detail_id,
        drug_source_value,
        drug_source_concept_id,
        route_source_value,
        dose_unit_source_value
      )
    )
  ) AS drug_exposures_json
FROM `bigquery-public-data.cms_synthetic_patient_data_omop.drug_exposure`
GROUP BY person_id,
  drug_concept_id

4. Using the created table, calculate the total number of individual drug exposures per person_id and drug_concept_id. Order by largest exposure count.
(Hint: use JSON_QUERY_ARRAY to convert the JSON field into a native array, then use ARRAY_LENGTH.)

5. Identify all person_id and drug_concept_id pairs where any of the individual drug exposures (in the native JSON field) had a days_supply greater than 30 (indicating a long-term prescription). For these specific groupings, calculate the average days_supply for only the exposures that meet the greater-than-30-day criterion.
(Hint: UNNEST the result of JSON_QUERY_ARRAY to flatten the JSON structure. You'll be able to use JSON_VALUE to extract specific elements by their key name but be aware that the value is always a STRING.)

-----------------------

Challenge:

Going back to the INFORMATION_SCHEMA.JOBS view, identify the top 5 completed QUERY jobs (in the last 7 days) that had the single longest-running execution stage. The job_stages field has details on each execution stage. For each of these 5 jobs, return the job ID, the total job duration, the ID of the single longest stage within that job, and that stage's duration in seconds.
(Hint: you can use start_ms and end_ms to calculated the duration of each stage. You'll also need to flatten the job stages array with UNNEST.)

