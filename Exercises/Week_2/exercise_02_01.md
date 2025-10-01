## Week 2, Part 1: Exploring Execution Plans

In this set of exerices, you'll compare the execution plans and efficiency of queries. 

You may find [the Postgres documentation](https://www.postgresql.org/docs/current/using-explain.html) helpful in reading the outputs.

1. Which columns from the person table have an index?

2. Compare the output from these two queries. What is different about the query plans? Why were the query plans different, even though the query results are identical?

Query 1:
EXPLAIN ANALYZE
SELECT *
FROM person
WHERE person_id = 34;

Query 2:
EXPLAIN ANALYZE
SELECT *
FROM person
WHERE person_id_no_idx = 34;

3. Compare the output from these two queries. What is different about the query plans? Why were the query plans different, even though the structure of the queries is similar?

Query 1:
EXPLAIN ANALYZE
SELECT *
FROM person
WHERE person_id < 1000;

Query 2:
EXPLAIN ANALYZE
SELECT *
FROM person
WHERE person_id > 1000;

4. Inspect the execution plan for the following query:

EXPLAIN ANALYZE
SELECT *
FROM person
WHERE person_id = 34
   OR person_id = 35
   OR person_id = 36
   OR person_id = 37
   OR person_id = 38;

Then rewrite the query using the IN keyword and inspect the new execution plan. What do you find?

Compare the results when you use the column with no index (person_id_no_idx).

5. The visit_start_date column from the visit_occurrence table has an index on it. Let's say we want to find all rows whose start date in in January 2009. We might start by using the extract function as in the following query: 

EXPLAIN ANALYZE
SELECT *
FROM visit_occurrence
WHERE EXTRACT(YEAR FROM visit_start_date) = 2009 AND EXTRACT(MONTH FROM visit_start_date) = 1;

Does this query use the index? Can you rewrite it so that the execution plan can take advantage of the index? 


6. Now, compare what happens if we filter for all records in 2009. Try it using EXTRACT:

EXPLAIN ANALYZE
SELECT *
FROM visit_occurrence
WHERE EXTRACT(YEAR FROM visit_start_date) = 2009;

Then rewrite the query to use the index. How much does the speedup compare to the previous question where you were filtering to just one month?

7. Let's say we want to count the number of rows each person has related to Type 2 diabetes mellitus (condition_concept_id = 201826).

One way we can do this is a simple join and aggregation:

SELECT p.person_id, COUNT(condition_concept_id)
FROM person p
LEFT JOIN condition_occurrence c
ON p.person_id = c.person_id
WHERE c.condition_concept_id = 201826
GROUP BY p.person_id;

Look at the query plan for this query.


10. Usually, we want to avoid [correlated subqueries](https://www.geeksforgeeks.org/sql/sql-correlated-subqueries/) but there can be times when they actually run faster than an uncorrelated version.

EXPLAIN ANALYZE
SELECT p.person_id,
       (
         SELECT COUNT(*)
         FROM condition_occurrence c
         WHERE c.person_id = p.person_id
           AND c.condition_concept_id = 201826 
       ) AS diabetes_condition_count,
       (
         SELECT COUNT(*)
         FROM drug_exposure d
         WHERE d.person_id = p.person_id
           AND d.drug_concept_id = 221344
       ) AS vaccine_count
FROM person p;

First, if we want to convert the correlated subquery into joins, what is wrong with this query:

SELECT 
	p.person_id, 
	COUNT(condition_concept_id) AS diabetes_count,
	COUNT(drug_concept_id) AS vaccine_count
FROM person p
LEFT JOIN condition_occurrence c
ON p.person_id = c.person_id
LEFT JOIN drug_exposure d
ON p.person_id = d.person_id
WHERE c.condition_concept_id = 201826 AND d.drug_concept_id = 2213440
GROUP BY p.person_id;


Now, if instead of one main query, we could perform counts using CTEs.

WITH condition_counts AS (
    SELECT person_id, COUNT(*) AS diabetes_condition_count
    FROM condition_occurrence
    WHERE condition_concept_id = 201826
      AND person_id IN (SELECT person_id FROM person)
    GROUP BY person_id
),
drug_counts AS (
    SELECT person_id, COUNT(*) AS vaccine_count
    FROM drug_exposure
    WHERE drug_concept_id = 2213440
      AND person_id IN (SELECT person_id FROM person)
    GROUP BY person_id
)
SELECT p.person_id,
       COALESCE(c.diabetes_condition_count, 0),
       COALESCE(d.vaccine_count, 0)
FROM person p
LEFT JOIN condition_counts c USING (person_id)
LEFT JOIN drug_counts d USING (person_id);

You'll notice that this takes a lot longer to run. Inspect the query plan to see why. 

More than likely, the planner is using a [Nested Loop Left Join](https://pganalyze.com/docs/explain/join-nodes/nested-loop), which is very inefficient. Unfortunaly, it thinks this will be the more efficient type of merge, but in this case will be very slow, and we're actually better off with a correlated subquery. 

Note that part of the reason that the correlated version was so much faster was the indexes. Try running it with no index instead:

SELECT p.person_id_no_idx,
       (
         SELECT COUNT(*)
         FROM condition_occurrence c
         WHERE c.person_id_no_idx = p.person_id_no_idx
           AND c.condition_concept_id = 201826 
       ) AS diabetes_condition_count,
       (
         SELECT COUNT(*)
         FROM drug_exposure d
         WHERE d.person_id_no_idx = p.person_id_no_idx
           AND d.drug_concept_id = 221344
       ) AS vaccine_count
FROM person p;

Does it work if one of the tables has an index?
