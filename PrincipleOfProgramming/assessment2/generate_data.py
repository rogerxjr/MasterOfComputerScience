import pandas as pd
import random

# ==========================================
# Configuration
# ==========================================
NUM_STUDENTS = 50  # Generate 50 records

# Define Options (Must match your questions.txt exactly)
# The first item in each list is the CORRECT answer (for my logic below)
q1_options = ["Rice cooked in coconut milk", "Noodles", "Bread", "Porridge"]
q2_options = ["Satay", "Laksa", "Roti Canai", "Char Kway Teow"]
q3_options = ["All of the above", "Penang", "Johor", "Sarawak"]
q4_options = ["Laksa", "Hokkien Mee", "Mee Goreng", "Cendol"]

# Correct Answers Mapping
correct_map = [
    "Rice cooked in coconut milk",
    "Satay",
    "All of the above",
    "Laksa"
]

# Student Names Pool
first_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", 
               "Kevin", "Laura", "Mike", "Nina", "Oscar", "Peggy", "Quinn", "Rupert", "Sybil", "Ted",
               "Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin", "Lucas", "Henry", "Alexander"]

# ==========================================
# Data Generation Logic
# ==========================================
data = []

print(f"Generating data for {NUM_STUDENTS} students...")

for i in range(NUM_STUDENTS):
    # 1. Generate Name
    name = f"{random.choice(first_names)} {random.randint(100, 999)}"
    
    # 2. Simulate Answers (Weighted Random)
    # We give a 70% weight to the correct answer (index 0), and 10% to others.
    # This simulates a realistic class performance.
    
    # Q1
    ans1 = random.choices(q1_options, weights=[0.7, 0.1, 0.1, 0.1], k=1)[0]
    
    # Q2
    ans2 = random.choices(q2_options, weights=[0.7, 0.1, 0.1, 0.1], k=1)[0]
    
    # Q3
    ans3 = random.choices(q3_options, weights=[0.7, 0.1, 0.1, 0.1], k=1)[0]
    
    # Q4
    ans4 = random.choices(q4_options, weights=[0.7, 0.1, 0.1, 0.1], k=1)[0]
    
    # 3. Calculate Score
    score = 0
    if ans1 == correct_map[0]: score += 1
    if ans2 == correct_map[1]: score += 1
    if ans3 == correct_map[2]: score += 1
    if ans4 == correct_map[3]: score += 1
    
    # Append to list
    data.append([name, score, ans1, ans2, ans3, ans4])

# ==========================================
# Save to CSV
# ==========================================
df = pd.DataFrame(data, columns=["Name", "Score", "Q1_Ans", "Q2_Ans", "Q3_Ans", "Q4_Ans"])
df.to_csv("results.csv", index=False)

print("✅ Success! 'results.csv' has been created with fake data.")
print(df.head())
