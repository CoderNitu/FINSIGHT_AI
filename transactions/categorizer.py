# This is our default, fallback dictionary
DEFAULT_KEYWORD_TO_CATEGORY = {
        'zomato': 'Food', 'swiggy': 'Food', 'restaurant': 'Food',
        'grocery': 'Groceries', 'bigbasket': 'Groceries', 'zepto': 'Groceries',
        'uber': 'Transport', 'ola': 'Transport', 'fuel': 'Transport',
        'electricity': 'Bills', 'recharge': 'Bills', 'airtel': 'Bills',
        'netflix': 'Entertainment', 'spotify': 'Entertainment',
        'amazon': 'Shopping', 'flipkart': 'Shopping', 'myntra': 'Shopping',
        'pharmacy': 'Health', 'apollo': 'Health',
        'salary': 'Salary',
    }
    
class TransactionCategorizer:
        def __init__(self, user_categories, user_keywords):
            """
            user_categories: A queryset of the user's Category objects.
            user_keywords: A queryset of the user's Keyword objects.
            """
            self.category_map = {category.name.lower(): category.id for category in user_categories}
            # Note the structure: keyword text maps to the category NAME
            self.user_keyword_map = {keyword.text.lower(): keyword.category.name.lower() for keyword in user_keywords}
    
        def suggest_category(self, description):
            description_lower = description.lower()
    
            # --- STEP 1: Check User's Custom Rules First ---
            for keyword, category_name in self.user_keyword_map.items():
                if keyword in description_lower:
                    if category_name in self.category_map:
                        return self.category_map[category_name]
    
            # --- STEP 2: If no custom match, check Default Rules ---
            for keyword, category_name in DEFAULT_KEYWORD_TO_CATEGORY.items():
                if keyword in description_lower:
                    if category_name.lower() in self.category_map:
                        return self.category_map[category_name.lower()]
            
            return None
    

