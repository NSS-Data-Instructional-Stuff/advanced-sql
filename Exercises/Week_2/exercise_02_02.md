## Week 2, Part 2: Improving Queries

#### Part 1
Each of the following queries produces the correct result, but are written in ways that make them inefficient, hard to maintain, or needlessly complex. Your task for each query is to understand what it is doing and then do the following. First, rewrite the query so that it produces the same result but is clearer (simplify the structure, remove unnecessary steps, and make the logic easy to follow) and more efficient (reduce redundant joins, avoid correlated subqueries, and eliminate unnecessary functions or other constructs that slow performance). Second, document your changes, identifying any inefficiencies or anti-patterns in your original query. Last, compare the performance of the original and revised queries using EXPLAIN ANALYZE to see the runtime before and after changes and to identify which parts of the changes had the biggest performance impact.


1. 

SELECT DISTINCT p.gender_concept_id, COUNT(DISTINCT v.visit_occurrence_id)
FROM person p
LEFT JOIN visit_occurrence v ON p.person_id = v.person_id
LEFT JOIN condition_occurrence c ON v.visit_occurrence_id = c.visit_occurrence_id
GROUP BY p.gender_concept_id;

2.

WITH all_visits AS (
    SELECT person_id, visit_start_date
    FROM visit_occurrence
),
earliest_visit AS (
    SELECT person_id, MIN(visit_start_date) AS first_visit_date
    FROM all_visits
    GROUP BY person_id
),
latest_visit AS (
    SELECT person_id, MAX(visit_start_date) AS last_visit_date
    FROM all_visits
    GROUP BY person_id
),
combined AS (
    SELECT e.person_id, e.first_visit_date, l.last_visit_date
    FROM earliest_visit e
    INNER JOIN latest_visit l ON e.person_id = l.person_id
)
SELECT DISTINCT person_id, first_visit_date, last_visit_date
FROM combined
ORDER BY person_id;

3. 
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

4.

SELECT p.person_id,
       CASE
           WHEN (
               EXTRACT(YEAR FROM (
                   SELECT MIN(v.visit_start_date)
                   FROM visit_occurrence v
                   WHERE v.person_id = p.person_id
               )) - p.year_of_birth
           ) < 18 THEN 'Child'
           WHEN (
               EXTRACT(YEAR FROM (
                   SELECT MIN(v.visit_start_date)
                   FROM visit_occurrence v
                   WHERE v.person_id = p.person_id
               )) - p.year_of_birth
           ) BETWEEN 18 AND 64 THEN 'Adult'
           WHEN (
               EXTRACT(YEAR FROM (
                   SELECT MIN(v.visit_start_date)
                   FROM visit_occurrence v
                   WHERE v.person_id = p.person_id
               )) - p.year_of_birth
           ) >= 65 THEN 'Senior'
           ELSE 'Unknown'
       END AS age_group
FROM person p;

5. 

SELECT t1.person_id, t1.avg_age_at_visit
FROM (
  SELECT v.person_id,
         AVG(EXTRACT(YEAR FROM v.visit_start_date) - p.year_of_birth) AS avg_age_at_visit
  FROM (
    SELECT * FROM visit_occurrence
    WHERE visit_concept_id = 9201 OR visit_concept_id = 9202 OR visit_concept_id = 9203
  ) v
  JOIN person p ON v.person_id = p.person_id
  GROUP BY v.person_id
) t1
JOIN person p2 ON t1.person_id = p2.person_id
WHERE p2.year_of_birth IS NOT NULL;


#### Part 2
The following queries have some subtle mistakes. Can you spot them and correct the query?

6. 
The intended purpose of this query is to find all patients who were prescribed oxygen (drug_concept_id = 19025280) and for those patients show all conditions they have had since 2010.

SELECT p.person_id,
       d.drug_concept_id,
       c.condition_concept_id
FROM person p
JOIN drug_exposure d ON p.person_id = d.person_id
JOIN condition_occurrence c ON p.person_id = c.person_id
WHERE d.drug_concept_id = 19025280
  AND c.condition_start_date >= DATE '2010-01-01';

7. 
The intended purpose of this query is to list all patients who were diagnosed with diabetes mellitus (condition_concept_id = 201820) and show the earliest date of occurrence.

SELECT p.person_id, MIN(condition_start_date)
FROM condition_occurrence c
INNER JOIN person p
ON c.person_id = c.person_id
WHERE condition_concept_id = 201820
GROUP BY p.person_id;

8. 
The intended purpose of this query is to list all patients who were prescribed rabeprazole sodium (drug_concept_id = 40163286) and show the date of the visit during which the drug was administered.

SELECT p.person_id, d.drug_concept_id, v.visit_start_date
FROM person p
JOIN drug_exposure d ON p.person_id = d.person_id
JOIN visit_occurrence v ON d.drug_exposure_start_date = v.visit_start_date
WHERE d.drug_concept_id = 40163286;
