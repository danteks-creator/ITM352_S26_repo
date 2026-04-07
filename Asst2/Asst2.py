import pandas as pd
import time
import sys

# Note: I used AI to " get my code and make it more defensive, maintainable, and user-friendly."
# Note: When using the custom data set function, use this link to access the alternate dataset: 
# https://drive.google.com/file/d/1bYlYj2isiMAyP4gUcgF8hhfKMMFEOgYg/view?usp=sharing
# I also asked AI "implement a summary of data, and create an alternate dataset"
# For maintainability, this script uses a modular design. To add new analytics, 
# you only need to add a tuple to the 'options' list in get_filtered_menu().

def load_sales_data(drive_url):
    # R1: Loading sales data. 
    # DEFENSIVE PROGRAMMING: The function handles potential for broken links or 
    # inaccessible files to ensure the program exits gracefully rather than crashing.
    print("\n" + "="*50)
    print("USER INTERFACE: Initializing connection to data source...")
    
    try:
        # DEFENSIVE: Extracts ID and rebuilds URL to ensure direct download from Google Drive.
        file_id = drive_url.split('/')[-2]
        direct_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        
        start_time = time.perf_counter()
        df = pd.read_csv(direct_url)
        
        # QUALITY: Normalize headers to lowercase and strip spaces for defensive formatting.
        # This prevents "Field Not Found" errors due to inconsistent CSV formatting.
        df.columns = df.columns.str.strip().str.lower()
        
        # STYLE: Standardize 'state' field to 'customer_state' for internal naming conventions.
        if 'state' in df.columns:
            df.rename(columns={'state': 'customer_state'}, inplace=True)
        
        # DEFENSIVE PROGRAMMING: Replaces all 'NaN' or null values with 0.
        # This ensures that math operations (sum/mean) in pivot tables do not fail.
        df.fillna(0, inplace=True)
        
        load_time = time.perf_counter() - start_time
        print(f"USER INTERFACE: Data loaded successfully in {load_time:.4f}s.")
        
        display_data_summary(df)
        return df

    except Exception as e:
        # DEFENSIVE: Catch-all for network issues or file permission errors.
        print(f"CRITICAL ERROR: Data access failed. {e}")
        return None

def display_data_summary(df):
    # USER INTERFACE: Provides an overview of the data (R1).
    # Defensive existence checks are used for every metric to prevent crashes if columns are missing.
    print("-" * 50)
    print("            DATASET SUMMARY REPORT")
    print("-" * 50)
    
    total_orders = len(df)
    unique_emps  = df['employee_name'].nunique() if 'employee_name' in df.columns else 0
    regions      = ", ".join(df['sales_region'].unique()) if 'sales_region' in df.columns else "N/A"
    
    # DEFENSIVE: Uses 'coerce' to handle badly formatted date strings.
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        date_range = f"{df['order_date'].min().date()} to {df['order_date'].max().date()}"
    else:
        date_range = "N/A"

    metrics = [
        ("Total Orders", total_orders),
        ("Number of Employees", unique_emps),
        ("Sales Regions", regions),
        ("Date Range", date_range),
        ("Unique Customers", df['customer_name'].nunique() if 'customer_name' in df.columns else 0),
        ("Product Categories", ", ".join(df['product_category'].unique()) if 'product_category' in df.columns else "N/A"),
        ("Unique States", df['customer_state'].nunique() if 'customer_state' in df.columns else 0),
        ("Total Sales Amount", f"${df['unit_price'].sum() if 'unit_price' in df.columns else 0:,.2f}"),
        ("Total Quantities Sold", f"{df['quantity'].sum() if 'quantity' in df.columns else 0:,}")
    ]
    
    for label, val in metrics:
        print(f"{label:<25}: {val}")
    print("-" * 50)

# R3: PREDEFINED ANALYTICAL TASKS
# QUALITY: Each task is organized into a custom function to increase flexibility and readability.

def task_show_rows(df):
    # USER INPUT VALIDATION: Checks that requested rows are within actual data bounds.
    total = len(df)
    print(f"\nEnter rows to display:\n- Enter a number 1 to {total}\n- To see all rows, enter 'all'\n- To skip preview, press Enter")
    choice = input("Your choice: ").strip().lower()
    if choice == "all":
        print(df)
    elif choice.isdigit():
        n = int(choice)
        print(df.head(n) if n <= total else f"Error: Only {total} rows available.")

def task_sales_region_order_type(df):
    # R3: Pivot aggregating sales by region and order_type (Retail/Wholesale).
    print(pd.pivot_table(df, values='unit_price', index='sales_region', columns='order_type', aggfunc='sum'))

def task_avg_sales_region_state_type(df):
    # R3: Pivot aggregating avg sales by region, state, and sale type.
    print(pd.pivot_table(df, values='unit_price', index='sales_region', columns=['customer_state', 'order_type'], aggfunc='mean'))

def task_sales_cust_order_state(df):
    # R3: Pivot showing sales by customer type and order type by state.
    print(pd.pivot_table(df, values='unit_price', index='customer_state', columns=['customer_type', 'order_type'], aggfunc='sum'))

def task_qty_price_region_product(df):
    # R3: Pivot showing sales qty and price by region and product.
    print(pd.pivot_table(df, values=['quantity', 'unit_price'], index=['sales_region', 'product_category'], aggfunc='sum'))

def task_qty_price_customer_type(df):
    # R3: Pivot showing sales qty and price by order and customer type.
    print(pd.pivot_table(df, values=['quantity', 'unit_price'], index=['order_type', 'customer_type'], aggfunc='sum'))

def task_max_min_category(df):
    # R3: Pivot showing max and min sales price by category.
    print(pd.pivot_table(df, values='unit_price', index='product_category', aggfunc=['max', 'min']))

def task_unique_employees_by_region(df):
    # R3: Pivot counting unique employees by region.
    print(pd.pivot_table(df, values='employee_name', index='sales_region', aggfunc=pd.Series.nunique))

def task_custom_pivot_generator(df):
    # R4: Custom Pivot Table Generator with interactive selections.
    # QUALITY: Handles validation for user choices and checks column existence.
    print("\n" + "="*30)
    print("   CUSTOM PIVOT GENERATOR")
    print("="*30)
    
    def get_user_selections(options, prompt):
        print(f"\n{prompt}")
        for i, opt in enumerate(options, 1): print(f"{i}. {opt}")
        ans = input("Enter choice(s) separated by commas: ").strip()
        try:
            indices = [int(x.strip()) - 1 for x in ans.split(',') if x.strip().isdigit()]
            return [options[i] for i in indices if 0 <= i < len(options)]
        except: return []

    rows = get_user_selections(['employee_name', 'sales_region', 'product_category', 'customer_state'], "Select Rows:")
    vals = get_user_selections(['quantity', 'unit_price'], "Select Values:")
    
    print("\nSelect Aggregation: 1. sum, 2. mean, 3. count")
    agg_map = {"1": "sum", "2": "mean", "3": "count"}
    agg_choice = agg_map.get(input("Choice: "), "sum")

    if rows and vals:
        print(pd.pivot_table(df, values=vals, index=rows, aggfunc=agg_choice))
    else:
        print("USER ERROR: Rows and Values must be selected. Returning to menu.")

def task_exit_dashboard(df):
    # Closes the application with a message.
    sys.exit("Exiting Dashboard. Goodbye!")

# --- R2: MENU LOGIC ---

def get_filtered_menu(df):
    # MAINTAINABILITY: Implements the menu in a general way (tuple of tuples).
    # Logic: (Label, Function, [Required Columns])
    options = (
        ("Show the first n rows of sales data", task_show_rows, []),
        ("Total sales by region and order_type", task_sales_region_order_type, ['sales_region', 'order_type', 'unit_price']),
        ("Average sales by region with average sales by state and sale type", task_avg_sales_region_state_type, ['sales_region', 'customer_state', 'order_type', 'unit_price']),
        ("Sales by customer type and order type by state.", task_sales_cust_order_state, ['customer_state', 'customer_type', 'order_type', 'unit_price']),
        ("Total sales quantity and price by region and product", task_qty_price_region_product, ['sales_region', 'product_category', 'quantity', 'unit_price']),
        ("Total sales quantity and price customer type", task_qty_price_customer_type, ['order_type', 'customer_type', 'quantity', 'unit_price']),
        ("Max and min sales price of sales by category", task_max_min_category, ['product_category', 'unit_price']),
        ("Number of unique employees by region", task_unique_employees_by_region, ['employee_name', 'sales_region']),
        ("Create a custom pivot table", task_custom_pivot_generator, []),
        ("Exit", task_exit_dashboard, [])
    )
    
    # MAINTAINABILITY: Logic filters menu based on actual data presence.
    # Requirement: Remove analytic if required data columns are not available.
    filtered = [(label, func) for label, func, reqs in options if all(col in df.columns for col in reqs)]
    return tuple(filtered)

def run_application():
    # USER INTERFACE: Intuitive dataset selection menu.
    # QUALITY: Allows for alternate dataset loading or custom URL entry.
    print("--- DATASET SELECTION ---")
    print("1. Use default Sales Data")
    print("2. Use alternate Sales Data (Google Drive)")
    print("3. Enter custom Google Drive URL")
    
    choice = input("Select (1-3): ").strip()
    
    # Handling Alternate Dataset Selection logic
    if choice == '2':
        url = "https://drive.google.com/file/d/1bYlYj2isiMAyP4gUcgF8hhfKMMFEOgYg/view?usp=sharing"
    elif choice == '3':
        url = input("Paste Google Drive Link: ").strip()
    else:
        url = "https://drive.google.com/file/d/1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA/view?usp=drive_link"

    sales_df = load_sales_data(url)
    
    if sales_df is not None:
        # QUALITY ASSURANCE: Generate the menu based on what the file actually supports.
        menu_items = get_filtered_menu(sales_df)
        while True:
            print("\n" + "="*40 + "\n--- Sales Data Dashboard ---\n" + "="*40)
            for i, (label, _) in enumerate(menu_items, 1):
                print(f"{i}. {label}")
            
            # USER INPUT VALIDATION: Checks for range and numeric input.
            sel = input("\nSelection: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(menu_items):
                menu_items[int(sel)-1][1](sales_df)
            else:
                print("USER ERROR: Please select a valid numeric option from the menu.")

if __name__ == "__main__":
    run_application()