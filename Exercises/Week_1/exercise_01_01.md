## Week 1, Part 1: Subquery and CTE Review

1. Find all patients whose age is greater than the average age of all patients. Hint: there is a year_of_birth column in the person table.

2. Find all patients with the condition type 2 diabetes mellitus. This condition is encoded using condition_concept_id = 201826 in the condition_occurrence table. Return the person_id and year_of_birth for these patients. Do this in two ways. First, join the person and condition_occurrence tables. Warning: make sure that you return each person_id only once. Then use a subquery with EXISTS. Which is faster?

3. For each patient in ther person table, find the number of different condition_concept_id values show up in the condition_occurrence table. Do this in two ways. First, use a join to connect the two tables. Then use a subquery in SELECT. The subquery in SELECT will have to be a [correlated subquery](https://www.geeksforgeeks.org/sql/sql-correlated-subqueries/). Note: make sure that you end up with 100000 rows in your result. Which version is faster?

4. For this question, use the drug_exposure table. For each drug concept, find the largest number of events for a single person associated with that drug. Your output should show that, for example, drug concept id 1301125 (epoetin alfa) had a patient with 332 events. 

5. Write a query to find the number of different drug concepts for each person. Then use this as a CTE to find all patients with more than 10 different drugs.

6. Using the visit_occurrence table, find all patients which have a higher number of visits than the average for their gender. Hint: write one CTE to find the total number of visits per patient. Then write a second CTE to find the average per gender.

7. For each patient, find the most recent visit.

8. Find patients who had a drug exposure before their first recorded condition diagnosis. Condition diagnoses can be found in the condition_occurrence table.