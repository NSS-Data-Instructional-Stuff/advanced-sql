## Week 4, Part 2: Lateral Joins

The first three questions use the cms patient data.

1. For each person in the person table, write a query which returns that person's person_id, year of birth, and the date and drug_concept_id for their first drug exposure.

2. Modify your previous query so that it finds the first drug exposure after that person turned 70. Hint: You may want to use the [MAKE_DATE function](https://www.postgresql.org/docs/current/functions-datetime.html).

3. Write a query which finds all drug exposures within 30 days of a visit. Include the drug_concept_id and drug_exposure_start_date. Bonus: Use JSON_AGG and JSON_BUILD_OBJECT so that you get one row per visit with potentially multiple drug exposures.

The next two questions use the neows dataset.

4. Write a query that returns the asteroid_id, name, and an array with the distinct bodies that it approaches. Hint: you can unnest in a lateral join. You may also want to use [array_agg](https://www.postgresql.org/docs/9.5/functions-aggregate.html) in your query.

5. Write a query that returns the asteroid_id and name and the date and distance of the closest approach to Earth. Hint: you may want to unpack the close approach data inside of a lateral join using [jsonb_array_elements](https://www.postgresql.org/docs/9.5/functions-json.html).

The final two questions use the Amazon Prime dataset.

6. Write a query that returns a table with the program title and the name of each actor or actress in that program, where each row contains only one actors (so a given program may have multiple rows). Hint: unnest in a lateral join.

7. Build off of your previous query to count the number of different titles that each actor or actress has appeared in.