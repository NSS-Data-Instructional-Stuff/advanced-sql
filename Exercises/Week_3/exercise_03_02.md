## Week 3, Part 2: Array and JSON Practice

1. Write a query which returns the asteroid_id, asteroid name and the is_potentially_hazardous_asteroid value for each asteroid in the dataset.

2. Modify the previous query to return the asteroid_id and names for all potentially hazardous asteroids in the dataset.

3. Find the average orbital period for asteroids in the dataset.

4. Write a query to find the asteroid_id, name, and the first observation date for each asteroid. Which asteroid has the earliest first observation date?

5. Find the date and relative velocity in miles per hour for the first close approach of each asteroid. Note: json arrays are zero-indexed in postgres.

6. For each asteroid, count the number of close approaches it has. Which has the most approaches?

7. Find all asteroids that have approached both Earth and Mars.

8. Find all asteroids that have approached Earth or Mars.

9. Find all asteroids that did not approach Earth.

10. Write a query that lists each asteroid_id and name with one approach body per row. Hint: Use unnest.

11. For each body, count how many different asteroids have approached.

**Challenge Questions**

1. Find the asteroid that has had the lowest miss distance to Earth. Hint: In order to answer this question, you may want to flatten the close approach data using jsonb_array_elements.

2. Find the date and relative velocity in miles per hour for the last close approach of each asteroid.

3. Find all asteroids that had a close approach in the year 2000. 

