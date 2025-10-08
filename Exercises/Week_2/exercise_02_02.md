## Week 2, Part 2: Improving Queries

Each of the following queries produces the correct result, but are written in ways that make them inefficient, hard to maintain, or needlessly complex. Your task for each query is to understand what it is doing and then do the following. First, rewrite the query so that it produces the same result but is clearer (simplify the structure, remove unnecessary steps, and make the logic easy to follow) and more efficient (reduce redundant joins, avoid correlated subqueries, and eliminate unnecessary functions or other constructs that slow performance). Second, document your changes, identifying any inefficiencies or anti-patterns in your original query. Last, compare the performance of the original and revised queries using EXPLAIN ANALYZE to see the runtime before and after changes and to identify which parts of the changes had the biggest performance impact.


1. 

SELECT DISTINCT p.gender_concept_id, COUNT(DISTINCT v.visit_occurrence_id)
FROM person p
JOIN visit_occurrence v ON p.person_id = v.person_id
JOIN condition_occurrence c ON v.visit_occurrence_id = c.visit_occurrence_id
GROUP BY p.gender_concept_id;

2. 
SELECT DISTINCT p.person_id,
       p.gender_concept_id,
       (
         SELECT COUNT(DISTINCT c.condition_concept_id)
         FROM condition_occurrence c
         JOIN person p2 ON c.person_id = p2.person_id
         WHERE p2.person_id = p.person_id
           AND c.condition_start_date >= '2010-01-01'
       ) AS num_conditions_2010
FROM person p
JOIN observation_period op ON op.person_id = p.person_id
WHERE op.observation_period_end_date >= '2010-07-01'
  AND p.year_of_birth < 1980;

3. 

SELECT p.person_id,
       CASE
         WHEN EXTRACT(YEAR FROM TO_DATE(p.year_of_birth::text || '-01-01', 'YYYY-MM-DD')) < 1970
              THEN 'Older'
         ELSE 'Younger'
       END AS age_group,
       d.drug_concept_id,
       d.drug_exposure_start_date
FROM person p
JOIN drug_exposure d 
  ON p.person_id = d.person_id
WHERE d.drug_exposure_start_date::text BETWEEN '2010-01-01' AND '2010-02-01'
  AND LOWER(p.gender_concept_id::text) = '8532';

4. 

SELECT t1.person_id, t1.avg_age_at_visit
FROM (
  SELECT v.person_id,
         AVG(EXTRACT(YEAR FROM v.visit_start_date) - p.year_of_birth) AS avg_age_at_visit
  FROM (
    SELECT * FROM visit_occurrence
    WHERE visit_concept_id = 9201 OR visit_concept_id = 9202 OR visit_concept_id = 9203)
  ) v
  JOIN person p ON v.person_id = p.person_id
  GROUP BY v.person_id
) t1
JOIN person p2 ON t1.person_id = p2.person_id
WHERE p2.year_of_birth IS NOT NULL;

5. 

SELECT p.person_id,
       p.gender_concept_id,
       CASE
         WHEN (
           SELECT COUNT(*)
           FROM drug_exposure d
           WHERE d.person_id = p.person_id
             AND d.drug_concept_id = 19077638
         ) > 0 THEN 'Yes'
         ELSE 'No'
       END AS took_glipizide
FROM person p
WHERE p.year_of_birth > 1960;


The following queries have some subtle mistakes. Can you spot them?


6.
SELECT p.person_id,
       d.drug_concept_id,
       c.condition_concept_id
FROM person p
JOIN drug_exposure d ON p.person_id = d.person_id
JOIN condition_occurrence c ON p.person_id = c.person_id
WHERE d.drug_concept_id = 1125315
  AND c.condition_start_date >= DATE '2010-01-01';

7. 
SELECT p.person_id, d.drug_concept_id, v.visit_start_date
FROM person p
JOIN drug_exposure d ON p.person_id = d.person_id
JOIN visit_occurrence v ON p.person_id = d.person_id
WHERE d.drug_concept_id = 19077638;



------------------------------------
Scratch work below

SELECT 
    p.person_id,
    p.gender_concept_id,
    (
        SELECT MAX(d2.drug_exposure_start_date)
        FROM drug_exposure d2
        WHERE d2.person_id = p.person_id
          AND d2.drug_concept_id = 19025280
    ) AS last_exposure
FROM person p
LEFT JOIN drug_exposure d1 ON p.person_id = d1.person_id
WHERE p.person_id IN (
    SELECT DISTINCT d3.person_id
    FROM drug_exposure d3
    WHERE CAST(d3.drug_exposure_start_date AS TEXT) LIKE '2009-02%'
)
ORDER BY p.person_id;

3. 

WITH people AS (
    SELECT person_id, gender_concept_id, year_of_birth
    FROM person
    WHERE year_of_birth IS NOT NULL
),
glipizide_exposures AS (
    SELECT person_id, drug_exposure_start_date
    FROM drug_exposure
    WHERE CAST(drug_concept_id AS TEXT) = '19077638'
),
recent_exposures AS (
    SELECT person_id, drug_exposure_start_date
    FROM drug_exposure
    WHERE EXTRACT(YEAR FROM drug_exposure_start_date)::TEXT >= '2010'
),
combined AS (
    SELECT DISTINCT m.person_id, m.drug_exposure_start_date
    FROM glipizide_exposures m
    LEFT JOIN recent_exposures r
      ON m.person_id = r.person_id
     AND DATE(m.drug_exposure_start_date) <= DATE(r.drug_exposure_start_date)
)
SELECT DISTINCT
    p.person_id,
    p.gender_concept_id,
    (
        SELECT COUNT(DISTINCT c.drug_exposure_start_date)
        FROM combined c
        WHERE c.person_id = p.person_id
    ) AS glipizide_count
FROM people p
LEFT JOIN drug_exposure d ON p.person_id = d.person_id
WHERE p.year_of_birth > 1960
  AND (CAST(d.drug_concept_id AS TEXT) LIKE '%1125315%' OR d.drug_concept_id IS NULL);