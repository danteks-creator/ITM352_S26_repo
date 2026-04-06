import pandas as pd
import time
import sys

# Note: I used AI to " get my code and make it more defensive, maintainable, and user-friendly."
# I also asked AI "implement a summary of data, and create an alternate dataset"
# I didn't really know what to do with the alternate dataset which is why I just asked AI to make it
# For maintainability, his script uses a modular design. To add new analytics, 
# you only need to add a tuple to the 'options' list in get_filtered_menu().

def load_sales_data(drive_url):
    
    # This is defensive, the function handles the potential for broken links or inaccessible files.
    # This ensures the program exits and doesn't crash.

    print("\n" + "="*50)
    print("USER INTERFACE: Initializing connection to data source...")
    
    try:
        # For defense, this extracts the ID and rebuilds the URL to ensure direct download from Google Drive regardless of the link type provided.
        file_id = drive_url.split('/')[-2]
        direct_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        
        start_time = time.perf_counter()
        df = pd.read_csv(direct_url)
        
        # For style and maintainability: Normalize headers to lowercase and strip spaces.
        # For defense, this prevents "Field Not Found" errors due to inconsistent CSV formatting.
        df.columns = df.columns.str.strip().str.lower()
        
        # STYLE / CONSISTENCY: Standardize the 'state' field to 'customer_state' 
        # as per specific project requirements for internal naming conventions.
        if 'state' in df.columns:
            df.rename(columns={'state': 'customer_state'}, inplace=True)
        
        # AI helped me make this more defensive
        # For defensive programming, replaces all 'NaN' or null values with 0.
        # This ensures that math operations (sum/mean) in pivot tables do not fail.
        df.fillna(0, inplace=True)
        
        load_time = time.perf_counter() - start_time
        print(f"USER INTERFACE: Data loaded successfully in {load_time:.4f}s.")
        
        display_data_summary(df)
        return df

    except Exception as e:
        # This is for defensive programming, it is a catch-all for network issues or file permission errors.
        # part of the things implemented when I asked AI to rewrite my code to make it more defensive.
        print(f"CRITICAL ERROR: Data access failed. {e}")
        return None

def display_data_summary(df):

   # Helps the user interface, provides an overview of the data 
   # I asked AI to make the summary look nicer and format it well

    print("-" * 50)
    print("           DATASET SUMMARY REPORT")
    print("-" * 50)
    
    # I asked AI how to make this summary more defensive, and it made existence checks.
    # This is for defensive reasons, uses existence checks for every metric. 
    # If a column is missing, the summary reports 'N/A' instead of crashing.
    total_orders = len(df)
    unique_emps  = df['employee_name'].nunique() if 'employee_name' in df.columns else 0
    regions      = ", ".join(df['sales_region'].unique()) if 'sales_region' in df.columns else "N/A"
    
    # This is for defensive reasons, uses 'coerce' to handle badly formatted date strings.
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        date_range = f"{df['order_date'].min().date()} to {df['order_date'].max().date()}"
    else:
        date_range = "N/A"

    # This builds the summary of the data, which is later printed.
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

# This part does the analysis of the data. It makes the pivot tables and other analytics based on the data given.

def task_show_rows(df):
    """
    USER INPUT VALIDATION: Checks that requested rows are within actual data bounds.
    """
    total = len(df)
    print(f"\nUSER INTERFACE: Enter 1 to {total}, 'all', or press Enter to skip.")
    choice = input("Your choice: ").strip().lower()
    if choice == "all": 
        print(df)
    elif choice.isdigit(): 
        # DEFENSIVE: Ensure the integer is valid for the current dataframe length.
        n = int(choice)
        print(df.head(n) if n <= total else f"Error: Only {total} rows available.")


def task_total_sales_by_region_order_type(df):
    pivot = pd.pivot_table(
        df,
        values='unit_price',
        index='sales_region',
        columns='order_type',
        aggfunc='sum'
    )
    print(pivot)


def task_avg_sales_by_region_state_type(df):
    pivot = pd.pivot_table(
        df,
        values='unit_price',
        index='sales_region',
        columns=['customer_state', 'order_type'],
        aggfunc='mean'
    )
    print(pivot)


def task_unique_employees_by_region(df):
    pivot = pd.pivot_table(
        df,
        values='employee_name',
        index='sales_region',
        aggfunc=pd.Series.nunique
    )
    print(pivot)


def task_custom_pivot_placeholder(df):
    print("\n[R4 Custom Generator Initialized...]")


def task_exit_dashboard(df):
    sys.exit("Exiting Dashboard. Goodbye!")

# --- DYNAMIC MENU MANAGEMENT ---

def get_filtered_menu(df):
    """
    QUALITY ASSURANCE: Implements the requirement to hide analytics if data is missing.
    By checking required columns here, we prevent the user from ever seeing 
    options that would cause an execution error.
    """
    #Displays label, function logic, required columns list
    options = [
        ("Show first n rows of sales data", task_show_rows, []),
        ("Total sales by region and order_type", 
         task_total_sales_by_region_order_type, 
         ['sales_region', 'order_type', 'unit_price']),
        
        ("Avg sales by region/customer_state/type", 
         task_avg_sales_by_region_state_type, 
         ['sales_region', 'customer_state', 'order_type', 'unit_price']),
        
        ("Unique employees by region", 
         task_unique_employees_by_region, 
         ['employee_name', 'sales_region']),
        
        ("Create a custom pivot table", task_custom_pivot_placeholder, [])
    ]
    
    # This is for maintainability, lists comprehension filters the menu based on actual data presence.
    filtered = [(label, func) for label, func, reqs in options if all(col in df.columns for col in reqs)]
    filtered.append(("Exit", task_exit_dashboard))
    return filtered

# Controls the application, makes sure only valid options can be selected and hanlds the main loop.

def run_application():
    """
    USER INTERFACE: Intuitive dataset selection menu.
    Allows for alternate data set loading as required.
    """
    print("--- DATASET SELECTION ---")
    print("1. Use default Sales Data (Google Drive)")
    print("2. Enter custom Google Drive URL")
    
    choice = input("Select (1-2): ").strip()
    # This is for input validation. if the user inputs something other than '1' or '2', it defaults to '1'.
    if choice == '2':
        url = input("Paste Google Drive Link: ").strip()
    else:
        url = "https://drive.google.com/file/d/1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA/view?usp=drive_link"

    sales_df = load_sales_data(url)
    
    if sales_df is not None:
        # For quality assurance, this generates the menu based on what the file actually supports.
        menu_items = get_filtered_menu(sales_df)
        while True:
            print("\n" + "="*40 + "\n   SALES ANALYTICS DASHBOARD\n" + "="*40)
            for i, (label, _) in enumerate(menu_items, 1):
                print(f"{i}. {label}")
            
            # This is for user input validation, it checks for range and numeric input.
            sel = input("\nSelection: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(menu_items):
                menu_items[int(sel)-1][1](sales_df)
            else:
                print("USER ERROR: Please select a valid numeric option from the menu.")
#conditional statement to run the application only if this script is executed directly
if __name__ == "__main__":
    run_application()