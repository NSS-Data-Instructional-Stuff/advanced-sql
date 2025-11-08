## BigQuery String Functions and Views

You'll use the new_york_trees dataset in BigQuery's public datasets to complete these exercises. Use the 2015 census table unless otherwise directed.

1. Create a short, compound location ID. The format should be first 4 characters of tree_id + first 3 letters of boroname in uppercase. An example of expected format: 8054BRO for tree_id 80548 in boroname Bronx

2. Identify the tree type (the second word) from spc_common. If there is only one word, return the entire name. (Hint: you'll probably want to use a regex function)

3. Remove surrounding whitespace from spc_common, calculate the length, and filter for lengths greater than 15. Return unique values.

4. First create a dataset in your BigQuery sandbox project. Then create a logical view named "healthy_tree_stats" for simplified, normalized access to tree health. You should include tree_id, boroname, zipcode, and spc_common fields. (Hint: you can use a CASE statement to take the existing values and not only make them more meaningful but also clean up missing data. Health status Good should become "Vigorous", Fair should be "Stable", Poor becomes "At Risk", and null values should be replaced with "Unknown")

5. Using the logical view created in question 4 and the 2005 tree census table, find the count of "Vigorous" trees added after 2005 (ie, they appear in 2015 but not 2005). Include the first word of spc_common from the view. (Hint: the 2005 census has a different schema than 2015, think about the most logical joining column)

6. Create a materialized view for pre-aggregating the count of trees by species within each borough. Include the boroname and src_common columns, as well as the count of trees per borough and species. Note that a limitation of using the public datasets is that you can't create a materialized view directly from the table (it's in a different organization/project). A workaround for the purposes of this exercise is to copy the table to your dataset and create the materialized view on the copy. You can write a multi-part statement to do this. The first part will use the CREATE TABLE syntax in SQL from a query result (https://docs.cloud.google.com/bigquery/docs/tables). Separate the two parts with a semi-colon and you can run the CREATE TABLE statement in the same job as the CREATE MATERIALIZED VIEW statement. Contain all logic in the CREATE MATERIALIZED VIEW statement. (If you need to recreate the table or materialized view , you will need to drop or delete them first.)

7. Using the materialized view created in the previous question, find the top 5 most common species across NYC and their percentage of the total tree population. (Hint: the count will be by borough)

Challenge question:

1. For this question we'll rank streets by diversity of species present. First clean the address - you want to keep only the street name without the street number or leading spaces. (There are non-standard or incomplete addresses but for this exercise assume that there is a number followed by a space and then the street name.) For each resulting street name, count the number of distinct tree species (spc_common) located on that street. Assign a rank to streets by borough (boroname) based on the diversity count; the street with the largest number of distinct species should be rank = 1. Use the QUALIFY clause to return the top 3 most diverse streets for each borough. (Hint: use DENSE_RANK() in the window function)