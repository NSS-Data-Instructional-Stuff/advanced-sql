import random

def assign_to_groups(items, num_groups):
    # Create a shallow copy to avoid modifying the original list
    shuffled_items = list(items)
    
    # Randomly shuffle the items in place
    random.shuffle(shuffled_items)
    
    # Initialize X empty groups
    groups = [[] for _ in range(num_groups)]
    
    # Distribute the shuffled items sequentially across the groups
    for index, item in enumerate(shuffled_items):
        group_index = index % num_groups
        groups[group_index].append(item)
        
    return groups

students = ["Anamika", "Darren", "Erin", "Luca", "Manisha", "Meve", "Prathima", "Praveena", "Selamawit"]
absent = ["Cindy", "Grant", "Helana", "Narendra", "Rachel", "Sulu"]
num_groups = 4

result = assign_to_groups(students, num_groups)

# Print the resulting groups
for i, group in enumerate(result):
    print(f"Group {i + 1}: {group}")
