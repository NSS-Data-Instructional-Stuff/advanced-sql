## Week 2, Part 1: Exploring Execution Plans

In this set of exercises, you'll compare the execution plans and efficiency of queries. 

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

EXPLAIN ANALYZE
SELECT p.person_id, COUNT(condition_concept_id)
FROM person p
LEFT JOIN condition_occurrence c
ON p.person_id = c.person_id
WHERE c.condition_concept_id = 201826
GROUP BY p.person_id;

Look at the query plan for this query.

In some cases, it helps to filter first using a CTE. We can try it here using 

EXPLAIN ANALYZE
WITH filtered_conditions AS (
  SELECT *
  FROM condition_occurrence
  WHERE condition_concept_id = 201826
)
SELECT p.person_id, COUNT(fc.condition_concept_id)
FROM person p
LEFT JOIN filtered_conditions fc
  ON p.person_id = fc.person_id
GROUP BY p.person_id;

Does it help in this case? Stretch goal: try and understand the difference in the query plans for these two versions.

8. We can also do a version using [correlated subqueries](https://www.geeksforgeeks.org/sql/sql-correlated-subqueries/). Inspect the query plan for the correlated version. How does it differ? Is it faster or slower than the uncorrelated one?

EXPLAIN ANALYZE
SELECT p.person_id,
       (
         SELECT COUNT(*)
         FROM condition_occurrence c
         WHERE c.person_id = p.person_id
           AND c.condition_concept_id = 201826 
       ) AS diabetes_condition_count
FROM person p;	


9. While prefiltering may not have given a speedup in this case, prefiltering can be helpful sometimes.

Compare 

EXPLAIN ANALYZE
SELECT p.person_id, COUNT(condition_concept_id)
FROM person p
LEFT JOIN condition_occurrence c
ON p.person_id = c.person_id
WHERE c.condition_concept_id > 200000
GROUP BY p.person_id;

to 

EXPLAIN ANALYZE
WITH filtered_conditions AS (
  SELECT *
  FROM condition_occurrence
  WHERE condition_concept_id > 200000
)
SELECT p.person_id, COUNT(fc.condition_concept_id)
FROM person p
LEFT JOIN filtered_conditions fc
  ON p.person_id = fc.person_id
GROUP BY p.person_id;

Which is more efficient?