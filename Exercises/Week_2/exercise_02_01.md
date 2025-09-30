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

