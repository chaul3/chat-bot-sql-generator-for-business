"""
Sample CSV data from open data sources
"""
import pandas as pd
import os

def create_sample_sales_data():
    """Create sample sales data CSV"""
    sales_data = [
        {"Date": "2024-01-01", "Product": "Laptop", "Category": "Electronics", "Sales": 1200, "Quantity": 2, "Region": "North"},
        {"Date": "2024-01-02", "Product": "Mouse", "Category": "Electronics", "Sales": 25, "Quantity": 5, "Region": "South"},
        {"Date": "2024-01-03", "Product": "Keyboard", "Category": "Electronics", "Sales": 75, "Quantity": 3, "Region": "East"},
        {"Date": "2024-01-04", "Product": "Monitor", "Category": "Electronics", "Sales": 300, "Quantity": 1, "Region": "West"},
        {"Date": "2024-01-05", "Product": "Desk", "Category": "Furniture", "Sales": 450, "Quantity": 1, "Region": "North"},
        {"Date": "2024-01-06", "Product": "Chair", "Category": "Furniture", "Sales": 200, "Quantity": 2, "Region": "South"},
        {"Date": "2024-01-07", "Product": "Phone", "Category": "Electronics", "Sales": 800, "Quantity": 1, "Region": "East"},
        {"Date": "2024-01-08", "Product": "Tablet", "Category": "Electronics", "Sales": 600, "Quantity": 1, "Region": "West"},
        {"Date": "2024-01-09", "Product": "Headphones", "Category": "Electronics", "Sales": 150, "Quantity": 3, "Region": "North"},
        {"Date": "2024-01-10", "Product": "Webcam", "Category": "Electronics", "Sales": 100, "Quantity": 2, "Region": "South"}
    ]
    
    df = pd.DataFrame(sales_data)
    return df

def create_sample_customer_data():
    """Create sample customer data CSV"""
    customer_data = [
        {"CustomerID": 1, "Name": "Alice Johnson", "Age": 28, "City": "New York", "Spending": 5000, "Segment": "Premium"},
        {"CustomerID": 2, "Name": "Bob Smith", "Age": 35, "City": "Los Angeles", "Spending": 3200, "Segment": "Standard"},
        {"CustomerID": 3, "Name": "Carol Brown", "Age": 42, "City": "Chicago", "Spending": 7500, "Segment": "Premium"},
        {"CustomerID": 4, "Name": "David Wilson", "Age": 29, "City": "Houston", "Spending": 2100, "Segment": "Basic"},
        {"CustomerID": 5, "Name": "Eva Davis", "Age": 38, "City": "Phoenix", "Spending": 4800, "Segment": "Standard"},
        {"CustomerID": 6, "Name": "Frank Miller", "Age": 45, "City": "Philadelphia", "Spending": 6200, "Segment": "Premium"},
        {"CustomerID": 7, "Name": "Grace Lee", "Age": 31, "City": "San Antonio", "Spending": 3900, "Segment": "Standard"},
        {"CustomerID": 8, "Name": "Henry Taylor", "Age": 39, "City": "San Diego", "Spending": 1800, "Segment": "Basic"},
        {"CustomerID": 9, "Name": "Iris Clark", "Age": 27, "City": "Dallas", "Spending": 5500, "Segment": "Premium"},
        {"CustomerID": 10, "Name": "Jack Anderson", "Age": 33, "City": "San Jose", "Spending": 4100, "Segment": "Standard"}
    ]
    
    df = pd.DataFrame(customer_data)
    return df

def create_sample_employee_data():
    """Create sample employee data CSV"""
    employee_data = [
        {"EmployeeID": 1, "Name": "John Doe", "Department": "Engineering", "Salary": 75000, "Experience": 5, "Performance": 4.2},
        {"EmployeeID": 2, "Name": "Jane Smith", "Department": "Marketing", "Salary": 65000, "Experience": 3, "Performance": 4.5},
        {"EmployeeID": 3, "Name": "Mike Johnson", "Department": "Sales", "Salary": 70000, "Experience": 7, "Performance": 4.0},
        {"EmployeeID": 4, "Name": "Sarah Brown", "Department": "HR", "Salary": 60000, "Experience": 4, "Performance": 4.3},
        {"EmployeeID": 5, "Name": "Tom Wilson", "Department": "Engineering", "Salary": 80000, "Experience": 8, "Performance": 4.6},
        {"EmployeeID": 6, "Name": "Lisa Davis", "Department": "Finance", "Salary": 72000, "Experience": 6, "Performance": 4.1},
        {"EmployeeID": 7, "Name": "Chris Miller", "Department": "Marketing", "Salary": 68000, "Experience": 4, "Performance": 4.4},
        {"EmployeeID": 8, "Name": "Amy Taylor", "Department": "Sales", "Salary": 71000, "Experience": 5, "Performance": 4.2},
        {"EmployeeID": 9, "Name": "Kevin Lee", "Department": "Engineering", "Salary": 77000, "Experience": 6, "Performance": 4.5},
        {"EmployeeID": 10, "Name": "Emma Clark", "Department": "HR", "Salary": 63000, "Experience": 3, "Performance": 4.3}
    ]
    
    df = pd.DataFrame(employee_data)
    return df

def generate_all_sample_csvs(output_dir: str = "data/csv_files/"):
    """Generate all sample CSV files"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Create and save sample datasets
    sales_df = create_sample_sales_data()
    sales_df.to_csv(os.path.join(output_dir, "sales_data.csv"), index=False)
    
    customer_df = create_sample_customer_data()
    customer_df.to_csv(os.path.join(output_dir, "customer_data.csv"), index=False)
    
    employee_df = create_sample_employee_data()
    employee_df.to_csv(os.path.join(output_dir, "employee_data.csv"), index=False)
    
    print(f"Sample CSV files created in: {output_dir}")
    return {
        "sales": os.path.join(output_dir, "sales_data.csv"),
        "customers": os.path.join(output_dir, "customer_data.csv"),
        "employees": os.path.join(output_dir, "employee_data.csv")
    }

if __name__ == "__main__":
    generate_all_sample_csvs()
