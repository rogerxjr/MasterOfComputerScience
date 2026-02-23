# def tax_calculation_system():
#     """
#     Malaysian Income Tax Calculation System (2022)
#     Main logic controller for calculating annual income tax.
#     """
#     continue_program = True
    
#     while continue_program:
#         print("\n" + "="*50)
#         print("--- Malaysian Income Tax Calculation System (2022) ---")
#         print("="*50)
        
#         # --- Step 1: User Input (With Validation) ---
#         # .strip() removes leading/trailing whitespace
#         tax_file_no = input("Enter Tax File Number: ").strip()
#         name = input("Enter Name: ").strip()
        
#         # 1. Input: Basic Salary
#         while True:
#             try:
#                 basic_salary = float(input("Enter Basic Salary (RM): "))
#                 if basic_salary < 0:
#                     print("   Error: Salary cannot be negative.")
#                 else:
#                     break  # Input is valid, exit loop
#             except ValueError:
#                 print("   Error: Invalid input. Please enter a number.")

#         # 2. Input: Bonus
#         while True:
#             try:
#                 bonus = float(input("Enter Bonus (RM): "))
#                 if bonus < 0:
#                     print("   Error: Bonus cannot be negative.")
#                 else:
#                     break
#             except ValueError:
#                 print("   Error: Invalid input. Please enter a number.")

#         # 3. Input: Commission
#         while True:
#             try:
#                 commission = float(input("Enter Commission (RM): "))
#                 if commission < 0:
#                     print("   Error: Commission cannot be negative.")
#                 else:
#                     break
#             except ValueError:
#                 print("   Error: Invalid input. Please enter a number.")

#         # 4. Input: Other Incomes
#         while True:
#             try:
#                 other_incomes = float(input("Enter Other Incomes (RM): "))
#                 if other_incomes < 0:
#                     print("   Error: Income cannot be negative.")
#                 else:
#                     break
#             except ValueError:
#                 print("   Error: Invalid input. Please enter a number.")
            
#         # --- Step 2: Calculate Total Income ---
#         total_income = basic_salary + bonus + commission + other_incomes
#         print(f"[*] Total Annual Income: RM {total_income:,.2f}")
        
#         # --- Step 3: Relief Calculation (Menu System) ---
#         print("\n--- Tax Relief Declaration ---")
        
#         # Dictionary Structure: ID -> [Description, Max Limit]
#         relief_config = {
#             1: ["Self & Dependent", 9000], 
#             2: ["Education Fees (Self)", 7000],
#             3: ["Life Insurance", 3000],
#             4: ["Medical Expenses", 8000],
#             5: ["Lifestyle (Tech & Non-Tech)", 5000],
#             6: ["Sports Equipment", 500],
#             7: ["Domestic Travel", 1000],
#             8: ["EV Charging Facilities", 2500],
#             9: ["Ordinary Child Relief", 2000],
#             10: ["Disabled Child Relief", 6000],
#             11: ["Breastfeeding Equipment", 1000],
#             12: ["Education Fee for Child", 8000],
#             13: ["Disability (Self/Spouse)", 6000],
#             14: ["Pension (EPF)", 4000],
#             15: ["SOSCO/EIS", 350]
#         }

#         current_relief = 0.0 
#         print(f"[*] Starting Relief: RM {current_relief}")
    
#         # Display the menu options
#         print("\nAvailable Relief Categories:")
#         for key, value in relief_config.items():
#             print(f"{key}. {value[0]} (Max: RM {value[1]})")
#         print("0. Done (Finish Declaration)")

#         # Loop for relief selection
#         while True:
#             try:
#                 choice = int(input("\nEnter ID to claim (0 to finish): "))
                
#                 if choice == 0:
#                     break # Exit relief selection
                
#                 if choice in relief_config:
#                     item_name = relief_config[choice][0]
#                     limit = relief_config[choice][1]
                    
#                     # Inner loop to validate relief amount
#                     while True:
#                         try:
#                             amount = float(input(f"   Enter amount for '{item_name}': "))
#                             if amount < 0:
#                                 print("   Error: Amount cannot be negative.")
#                             else:
#                                 break
#                         except ValueError:
#                             print("   Error: Invalid number.")

#                     # Core Logic: Apply the minimum cap (Claim amount vs Limit)
#                     claimable = min(amount, limit)
                    
#                     # Accumulate total relief
#                     current_relief += claimable
#                     print(f"   >>> Added RM {claimable:,.2f} (Limit: {limit}). Total Relief: RM {current_relief:,.2f}")
#                 else:
#                     print("   Invalid ID. Please try again.")
                    
#             except ValueError:
#                 print("   Please enter a valid integer ID.")
        
#         total_relief = current_relief
        
#         # --- Step 4: Taxable Income Calculation ---
#         # Ensure taxable income is not negative using max(0, ...)
#         taxable_income = max(0, total_income - total_relief)
            
#         # --- Step 5: Tax Calculation Logic ---
#         tax_amount = 0
        
#         if taxable_income <= 5000:
#             # Tier 1: 0% Tax
#             tax_amount = 0
#         elif taxable_income <= 20000 :
#             # Tier 2: 1% Tax on amount above 5,000
#             tax_amount = (taxable_income - 5000) * 0.01
#         elif taxable_income <= 35000:
#             # Tier 3: RM 150 base + 3% on amount above 20,000
#             tax_amount = 150 + ((taxable_income - 20000) * 0.03)
#         else:
#             # Tier 4: RM 600 base + 8% on amount above 35,000
#             # Note: 150 + 450 = 600
#             tax_amount = 150 + 450 + ((taxable_income - 35000) * 0.08)
            
#         # --- Step 6: Output Results ---
#         # NOTE: This block is dedented to run for ALL tax tiers
#         print("\n" + "="*40)
#         print(f"TAX SUMMARY FOR: {name.upper()}")
#         print(f"Tax File No: {tax_file_no}")
#         print("-" * 40)
#         print(f"Total Income:       RM {total_income:,.2f}")
#         print(f"Total Relief:       RM {total_relief:,.2f}")
#         print(f"Taxable Income:     RM {taxable_income:,.2f}")
#         print("-" * 40)
#         print(f"TOTAL TAX PAYABLE:  RM {tax_amount:,.2f}")
#         print("="*40)
        
#         # --- Step 7: Loop Control ---
#         check = input("\nCalculate for another person? (yes/no): ").lower()
#         if check != 'yes':
#             continue_program = False
#             print("Exiting System. Thank you.")

# if __name__ == "__main__":
#     tax_calculation_system()

class Person:
    def __init__(self, name, id_no):
        self.__name = name      
        self.__id_no = id_no    

    def get_name(self):
        return self.__name

    def display_info(self):
        print(f"Name is: {self.__name}")
        print(f"IDNo is: {self.__id_no}")


class TaxPayer(Person):
    def __init__(self, name, id_no, tax_file_no, gross_income, epf_socso):
        super().__init__(name, id_no)  
        
        self.__tax_file_no = tax_file_no
        self.__gross_income = float(gross_income)
        self.__epf_socso = float(epf_socso)
        self.__expenses = {} 
        
        self.__calculator = TaxCalculation()

    def add_expense(self, category, amount):
        self.__expenses[category] = float(amount)

    def display_info(self):
        super().display_info() 
        print(f"Tax File No: {self.__tax_file_no}")

        total_relief = self.__calculator.calculate_total_relief(self.__expenses)
        chargeable_income = self.__calculator.calculate_taxable_income(
            self.__gross_income, total_relief, self.__epf_socso
        )
        
        tax_amount = self.__calculator.calculate_tax(chargeable_income)

        print(f"Gross Income      : RM {self.__gross_income:,.2f}")
        print(f"EPF/SOCSO Ded.    : RM {self.__epf_socso:,.2f}")
        print(f"Total Tax Relief  : RM {total_relief:,.2f}")
        print(f"Chargeable Income : RM {chargeable_income:,.2f}")
        print("="*40)

class TaxCalculation:
    def __init__(self):
        self.__relief_limits = {
            "self_dependent": 7000.00,
            "education_self": 7000.00,
            "life_insurance": 3000.00,
            "medical": 8000.00,
            "lifestyle": 5000.00,
            "sports_equipment": 500.00,
            "domestic_travel": 1000.00,
            "ev_charging": 2500.00,
            "child_relief": 2000.00,
            "child_disabled": 6000.00,
            "breastfeeding": 1000.00,
            "child_education": 8000.00,
            "disability_equipment": 6000.00,
            "epf": 4000.00,
            "socso": 350.00
        }


    def calculate_total_relief(self, expenses):
        total_relief = self.__relief_limits["self_dependent"]
        for category, amount in expenses.items():
            if category in self.__relief_limits:
                limit = self.__relief_limits[category]
                if category == "self_dependent":
                    continue
                claimable = min(amount, limit)
                total_relief += claimable
                
        return total_relief

    def calculate_taxable_income(self, gross_income, total_relief, epf_socso):
        income = gross_income - total_relief - epf_socso
        return max(0, income) 
    
    def calculate_tax(self, chargeable_income):
        if chargeable_income <= 5000:
            tax_amount = 0.0
        elif chargeable_income <= 20000 :
            tax_amount = (chargeable_income - 5000) * 0.01
        elif chargeable_income <= 35000:
            tax_amount = 150 + ((chargeable_income - 20000) * 0.03)
        else:
            tax_amount = 150 + 450 + ((chargeable_income - 35000) * 0.08)
        return tax_amount

class TaxSystem:
    def run(self):        
        test_user1 = TaxPayer("Roger", "1", "SG1001", 85000, 5000)
        test_user1.add_expense("lifestyle", 9000) 
        test_user1.add_expense("insurance", 3000)
        
        test_user2 = TaxPayer("RogerTWo", "2", "SG1002", 48000, 4000)
        test_user2.add_expense("education", 2000)
        test_user2.add_expense("medical", 1500)

        test_user3 = TaxPayer("RogerThree", "3", "SG1003", 24000, 2600)

        test_user4 = TaxPayer("ROgerFour", "4", "SG1004", 60000, 4500)
        test_user4.add_expense("lifestyle", 2500) 
        test_user4.add_expense("sports", 800)     
        test_user4.add_expense("medical", 9000)  

        taxpayers = [test_user1, test_user2, test_user3, test_user4]
        
        for user in taxpayers:
            user.display_info()

if __name__ == "__main__":
    system = TaxSystem()
    system.run()
