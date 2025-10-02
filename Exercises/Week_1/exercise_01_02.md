## Week 1, Part 2: Window Functions Practice

1. For each patient, find their first exposure to epoetin alfa (drug_concept_id = 1301125). Return a table that includes all column from the drug_exposure table.

2. For each person, count their visits and rank them within their gender.

3. For each patient, calculate a running total of visits over time, ordered by visit_start_date.

4. Show each patient's total number of different conditions and the average number of conditions across all patients in the same gender.

5. For each provider, give the percentage of the total epotin alfa (drug_concept_id = 1301125) prescribed by that provider. 

6. For each patient, identify inpatient or emergency visits that occur less than 30 days after the previous visit. These could indicate possible readmissions. Inpatient and emergency visits can be found using visit_concept_ids 9201 and 9203. 