## BigQuery String Functions

You'll use the new_york_trees dataset in BigQuery's public datasets to complete these exercises. Use the 2015 census table unless otherwise directed.

1. Create a short, compound location ID. The format should be first 4 characters of tree_id + first 3 letters of boroname in uppercase. An example of expected format: 8054BRO for tree_id 80548 in boroname Bronx

2. Identify the tree type (the second word) from spc_common. If there is only one word, return the entire name. (Hint: you'll probably want to use a regex function)

3. Remove surrounding whitespace from spc_common, calculate the length, and filter for lengths greater than 15. Return unique values.

4. Create a new column called latin_abbr. The columns should contain the first letter of the spc_latin genus (first word), followed by a period, a space, and the full species name (second word). An example: Cornus alternifolia becomes C. alternifolia.

Challenge question:

1. For this question we'll rank streets by diversity of species present. First clean the address - you want to keep only the street name without the street number or leading spaces. (There are non-standard or incomplete addresses but for this exercise assume that there is a number followed by a space and then the street name.) For each resulting street name, count the number of distinct tree species (spc_common) located on that street. Assign a rank to streets by borough (boroname) based on the diversity count; the street with the largest number of distinct species should be rank = 1. Use the QUALIFY clause to return the top 3 most diverse streets for each borough. (Hint: use DENSE_RANK() in the window function)