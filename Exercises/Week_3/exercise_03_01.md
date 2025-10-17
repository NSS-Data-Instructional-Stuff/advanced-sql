## Week 3, Part 1: Views and Functions Practice

1. In this exercise, you'll convert a query to both a view and function to encapsulate the same logic.  
a. Start by writing a query using the visit_occurrence table to find the total number of patients per provider, considering only inpatient visits (visit_concept_id=9201).
b. Convert your query into both a standard view and a materialized view.
c. Perform a select all from both views? Which is faster? 

2. Create a function that takes as input a person_id and returns a table showing drug_concept_id and total quantity of each of the drugs for that patient from the drug_exposure table. Then use your function to find the total quantity by drugs for person_id 2431. Then 

3. Modify the function you created in the last part so that it also takes two additional inputs, a start and end date, and returns the totals for all drug exposures with a drug_exposure_start_date between the supplied dates. Note: if you want to overwrite a function, you can use CREATE OR REPLACE FUNCTION. Then use your function to find the total quantity by drug for person_id 2431 with a drug_exposure_start_date in 2009.

4. In part 1, you counted number of inpatient patients per provider. Now make another one that gives all outpatient visits per provider (concept_id = 9202). Then write a query which joins the two views to compare inpatient vs. outpatient counts per provider. In this, make sure that you replace NULL values with 0.

5. Build a view that shows each patient's first inpatient visit date. Then use that view in a query that calculates how many patients had a follow-up visit within 90 days. Hint: You may want to make use of the [INTERVAL keyword](https://www.datacamp.com/doc/postgresql/interval).

## Challenge Questions

1. Write a function that takes an age threshold and returns the number of patients above that threshold who had inpatient visits. Note: when creating this function, you may want to change the return type. See [the CREATE FUNCTION documentation](https://www.postgresql.org/docs/current/sql-createfunction.html). Also, to determine a person's age, you may want to make use of the [MAKE_DATE function](https://www.postgresql.org/docs/current/functions-datetime.html). You may also want to use the [AGE function](https://www.geeksforgeeks.org/postgresql/postgresql-age-function/). How many people above the age of 90 had an inpatient visit? 

2. In this exercise, you'll chain together views.  
a. Start by creating a view to find all inpatient visits in 2009.
b. Then create a materialized view that counts distinct patients per provider from that filtered view.
c. Finally, write a query using the materialized view to get the top 5 providers by number of distinct patients in 2009.