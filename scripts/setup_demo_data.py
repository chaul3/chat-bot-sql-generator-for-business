"""
Quick setup script to download and prepare the Superstore dataset
This is the most recommended dataset for demonstrating the chatbot
"""
import os
import pandas as pd
import requests
from pathlib import Path

def download_superstore_dataset():
    """Download the Superstore dataset for demo purposes"""
    print("🏪 Setting up Superstore Dataset for your chatbot...")
    
    # Create datasets directory
    datasets_dir = Path("datasets")
    datasets_dir.mkdir(exist_ok=True)
    
    # Note: Since we can't directly download from Kaggle without API keys,
    # we'll create a comprehensive sample dataset based on the Superstore format
    print("📊 Creating sample Superstore-style dataset...")
    
    # Generate sample data that matches Superstore format
    import random
    from datetime import datetime, timedelta
    
    # Sample data generation
    regions = ['East', 'West', 'Central', 'South']
    states = ['California', 'Texas', 'Florida', 'New York', 'Illinois', 'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']
    cities = ['Los Angeles', 'New York City', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    categories = ['Technology', 'Furniture', 'Office Supplies']
    sub_categories = {
        'Technology': ['Phones', 'Computers', 'Tablets', 'Accessories'],
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Storage'],
        'Office Supplies': ['Binders', 'Paper', 'Pens', 'Art']
    }
    
    segments = ['Consumer', 'Corporate', 'Home Office']
    ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    
    # Generate sample data
    data = []
    base_date = datetime(2023, 1, 1)
    
    for i in range(1000):  # Generate 1000 sample records
        category = random.choice(categories)
        sub_category = random.choice(sub_categories[category])
        
        # Generate realistic sales and profit
        quantity = random.randint(1, 10)
        if category == 'Technology':
            unit_price = random.uniform(50, 2000)
            profit_margin = random.uniform(0.1, 0.3)
        elif category == 'Furniture':
            unit_price = random.uniform(100, 1500)
            profit_margin = random.uniform(0.05, 0.25)
        else:  # Office Supplies
            unit_price = random.uniform(5, 200)
            profit_margin = random.uniform(0.15, 0.4)
        
        sales = round(quantity * unit_price, 2)
        profit = round(sales * profit_margin, 2)
        
        order_date = base_date + timedelta(days=random.randint(0, 365))
        ship_date = order_date + timedelta(days=random.randint(1, 7))
        
        record = {
            'Row ID': i + 1,
            'Order ID': f'CA-{2023}-{str(i+1000000)[1:]}',
            'Order Date': order_date.strftime('%Y-%m-%d'),
            'Ship Date': ship_date.strftime('%Y-%m-%d'),
            'Ship Mode': random.choice(ship_modes),
            'Customer ID': f'CG-{random.randint(10000, 99999)}',
            'Customer Name': f'Customer {i+1}',
            'Segment': random.choice(segments),
            'Country': 'United States',
            'City': random.choice(cities),
            'State': random.choice(states),
            'Region': random.choice(regions),
            'Product ID': f'TEC-{category[:2].upper()}-{random.randint(1000, 9999)}',
            'Category': category,
            'Sub-Category': sub_category,
            'Product Name': f'{sub_category} Product {random.randint(1, 100)}',
            'Sales': sales,
            'Quantity': quantity,
            'Discount': round(random.uniform(0, 0.3), 2),
            'Profit': profit
        }
        data.append(record)
    
    # Create DataFrame and save
    df = pd.DataFrame(data)
    output_file = datasets_dir / "superstore_sample.csv"
    df.to_csv(output_file, index=False)
    
    print(f"✅ Dataset created: {output_file}")
    print(f"📈 Records: {len(df)} rows, {len(df.columns)} columns")
    print(f"💰 Total Sales: ${df['Sales'].sum():,.2f}")
    print(f"📊 Categories: {', '.join(df['Category'].unique())}")
    print(f"🌎 Regions: {', '.join(df['Region'].unique())}")
    
    # Create a summary file
    summary_file = datasets_dir / "dataset_info.txt"
    with open(summary_file, 'w') as f:
        f.write(f"Superstore Sample Dataset\n")
        f.write(f"========================\n\n")
        f.write(f"File: superstore_sample.csv\n")
        f.write(f"Records: {len(df)} rows\n")
        f.write(f"Columns: {len(df.columns)}\n")
        f.write(f"Total Sales: ${df['Sales'].sum():,.2f}\n")
        f.write(f"Date Range: {df['Order Date'].min()} to {df['Order Date'].max()}\n\n")
        f.write(f"Sample Questions to Try:\n")
        f.write(f"- What's the total sales by region?\n")
        f.write(f"- Which product category has the highest profit?\n")
        f.write(f"- Show me sales trends by month\n")
        f.write(f"- What's the average order value?\n")
        f.write(f"- Which customer segment is most profitable?\n")
        f.write(f"- Generate SQL for top 10 products by sales\n")
    
    print(f"📝 Info file created: {summary_file}")
    print("\n🚀 Ready to use with your chatbot!")
    print("\nNext steps:")
    print("1. Start your chatbot: .venv/bin/python -m streamlit run local_demo.py")
    print("2. Upload the CSV file using the sidebar")
    print("3. Try the sample questions listed above!")
    
    return output_file

if __name__ == "__main__":
    download_superstore_dataset()
