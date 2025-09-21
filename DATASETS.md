# 🎯 Recommended Toy Datasets for Your Chatbot

This guide provides curated datasets perfect for demonstrating your local database & CSV chatbot capabilities. All datasets are free, publicly available, and ideal for business intelligence and SQL query demonstrations.

## 📊 **Business & Sales Datasets**

### 1. **Superstore Dataset**  **HIGHLY RECOMMENDED**
- **Source**: Tableau Public / Kaggle
- **Download**: `https://www.kaggle.com/datasets/vivek468/superstore-dataset-final`
- **Size**: ~10K rows, ~21 columns
- **Perfect for**: Sales analysis, regional performance, product categories
- **Sample Questions**:
  - "What's our total profit by region?"
  - "Which product category has the highest sales?"
  - "Show me top 10 customers by revenue"
  - "Generate SQL for monthly sales trends"

### 2. **Northwind Database Sample**
- **Source**: Microsoft Sample Database
- **Download**: `https://github.com/Microsoft/sql-server-samples/tree/master/samples/databases/northwind-pubs`
- **Format**: SQL scripts + CSV exports
- **Perfect for**: Classic business scenarios (customers, orders, products, employees)
- **Sample Questions**:
  - "How many orders did we have last month?"
  - "Which employee has the highest sales?"
  - "Show supplier information for products"

### 3. **E-commerce Dataset**
- **Source**: Kaggle
- **Download**: `https://www.kaggle.com/datasets/carrie1/ecommerce-data`
- **Size**: ~540K rows
- **Perfect for**: Customer behavior, transaction analysis
- **Sample Questions**:
  - "What's the average order value?"
  - "Which country has the most customers?"
  - "Find customers who haven't ordered recently"

## 💼 **HR & Employee Datasets**

### 4. **HR Analytics Dataset**
- **Source**: Kaggle
- **Download**: `https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset`
- **Size**: ~1.5K employees, 35 attributes
- **Perfect for**: Employee analytics, attrition prediction
- **Sample Questions**:
  - "What's the average salary by department?"
  - "Which factors correlate with employee attrition?"
  - "Show employees with high performance ratings"

### 5. **Employee Database Sample**
- **Source**: MySQL Sample Database
- **Download**: `https://github.com/datacharmer/test_db`
- **Size**: ~300K employees
- **Perfect for**: Large-scale HR queries, department analysis
- **Sample Questions**:
  - "How many employees in each department?"
  - "What's the salary distribution?"
  - "Find employees hired in specific years"

## 🏥 **Healthcare & Medical**

### 6. **Healthcare Cost Dataset**
- **Source**: Kaggle
- **Download**: `https://www.kaggle.com/datasets/mirichoi0218/insurance`
- **Size**: ~1.3K records
- **Perfect for**: Cost analysis, demographic insights
- **Sample Questions**:
  - "What's the average insurance cost by region?"
  - "How does smoking affect insurance charges?"
  - "Show cost distribution by age groups"

## 🏠 **Real Estate & Housing**

### 7. **House Prices Dataset**
- **Source**: Kaggle
- **Download**: `https://www.kaggle.com/datasets/harlfoxem/housesalesprediction`
- **Size**: ~21K house sales
- **Perfect for**: Property analysis, market trends
- **Sample Questions**:
  - "What's the average price per square foot?"
  - "Which neighborhoods have highest prices?"
  - "Show price trends by year built"

## 🚗 **Transportation & Automotive**

### 8. **Car Sales Dataset**
- **Source**: Kaggle
- **Download**: `https://www.kaggle.com/datasets/syedanwarafridi/vehicle-sales-data`
- **Size**: ~16K vehicle sales
- **Perfect for**: Automotive industry analysis
- **Sample Questions**:
  - "Which car models sell the most?"
  - "What's the average price by manufacturer?"
  - "Show sales trends by year and model"

## 📈 **Financial & Stock Data**

### 9. **Stock Market Dataset**
- **Source**: Yahoo Finance / Kaggle
- **Download**: `https://www.kaggle.com/datasets/jacksoncrow/stock-market-dataset`
- **Perfect for**: Financial analysis, trend detection
- **Sample Questions**:
  - "What's the average daily volume?"
  - "Show stock performance comparisons"
  - "Find highest/lowest closing prices"

## 🎮 **Gaming & Entertainment**

### 10. **Video Game Sales**
- **Source**: Kaggle
- **Download**: `https://www.kaggle.com/datasets/gregorut/videogamesales`
- **Size**: ~16K games
- **Perfect for**: Entertainment industry analysis
- **Sample Questions**:
  - "Which gaming platform has highest sales?"
  - "Show sales by genre and year"
  - "Find top-selling games by region"

---

## 🛠️ **How to Use These Datasets with Your Chatbot**

### **Step 1: Download & Prepare**
```bash
# Create a datasets folder
mkdir datasets
cd datasets

# Download your chosen dataset (example: Superstore)
# Save as CSV file in the datasets folder
```

### **Step 2: Load into Your Chatbot**
```bash
# Start your local demo
.venv/bin/python -m streamlit run local_demo.py

# Use the file upload feature in the sidebar
# Or copy CSV to data/csv_files/ folder
```

### **Step 3: Test with Sample Questions**
- Upload the CSV file through the web interface
- Ask questions like those listed above
- Test both natural language queries and SQL generation
- Explore the dashboard and visualization features

### **Step 4: Database Integration (Optional)**
```python
# Convert CSV to SQLite database
import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv('your_dataset.csv')

# Save to database
conn = sqlite3.connect('your_dataset.db')
df.to_sql('main_table', conn, index=False, if_exists='replace')
conn.close()
```

## 📋 **Dataset Selection Guidelines**

### **Choose Based on Your Demo Goals:**
- **Business Intelligence**: Superstore, E-commerce, Northwind
- **HR Analytics**: IBM HR, Employee Database
- **Financial Analysis**: Stock Market, Insurance
- **General Purpose**: Superstore (most versatile)

### **Size Considerations:**
- **Small (< 1K rows)**: Quick demos, responsive interface
- **Medium (1K-10K)**: Good balance of complexity and performance
- **Large (> 10K)**: Stress testing, performance demonstrations

### **Column Variety:**
- **Numerical**: Sales amounts, quantities, prices, ratings
- **Categorical**: Regions, categories, departments, status
- **Dates**: Order dates, hire dates, transaction timestamps
- **Text**: Names, descriptions, addresses

## 🎯 **Pro Tips for Your Chatbot Demo**

1. **Start Simple**: Begin with Superstore dataset - it's perfect for demos
2. **Mix Data Types**: Choose datasets with numbers, categories, and dates
3. **Business Relevant**: Use datasets that reflect real business scenarios
4. **Test Queries**: Prepare sample questions that showcase your chatbot's capabilities
5. **Document Examples**: Create a list of impressive queries for demonstrations

---

**Happy Data Exploration! 📊🤖**
