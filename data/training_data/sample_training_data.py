"""
Training data generator for fine-tuning
"""

def get_sample_csv_questions():
    """Get sample questions for CSV data analysis"""
    return [
        "What's the total sales amount?",
        "Which product has the highest sales?",
        "What's the average age of customers?",
        "How many customers are in each segment?",
        "What's the distribution of sales by region?",
        "Which department has the highest average salary?",
        "What's the correlation between experience and salary?",
        "Show me the top 5 performing employees",
        "What's the average spending by customer segment?",
        "Which category generates the most revenue?",
        "What's the average quantity sold per product?",
        "How many employees are in each department?",
        "What's the relationship between age and spending?",
        "Show me sales trends over time",
        "Which region has the best sales performance?",
        "What's the employee performance distribution?",
        "How does experience correlate with performance?",
        "What's the total quantity sold by category?",
        "Which city has the most customers?",
        "What's the average sales per transaction?"
    ]

def get_additional_sql_questions():
    """Get additional SQL questions for training"""
    return [
        {
            "question": "Show me all customers from New York",
            "sql_query": "SELECT * FROM customers WHERE city = 'New York';"
        },
        {
            "question": "What's the total revenue by product category?",
            "sql_query": "SELECT category, SUM(price * stock_quantity) as total_revenue FROM products GROUP BY category;"
        },
        {
            "question": "Find customers who registered this year",
            "sql_query": "SELECT * FROM customers WHERE strftime('%Y', registration_date) = '2023';"
        },
        {
            "question": "Get the average order amount",
            "sql_query": "SELECT AVG(total_amount) as avg_order_amount FROM orders;"
        },
        {
            "question": "Show products that are out of stock",
            "sql_query": "SELECT * FROM products WHERE stock_quantity = 0;"
        },
        {
            "question": "List customers with their total order amounts",
            "sql_query": "SELECT c.name, SUM(o.total_amount) as total_spent FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.name;"
        },
        {
            "question": "Find the most popular product",
            "sql_query": "SELECT p.name, SUM(o.quantity) as total_sold FROM products p JOIN orders o ON p.product_id = o.product_id GROUP BY p.product_id, p.name ORDER BY total_sold DESC LIMIT 1;"
        },
        {
            "question": "Show orders from the last 30 days",
            "sql_query": "SELECT * FROM orders WHERE order_date >= date('now', '-30 days');"
        },
        {
            "question": "Get customer count by city",
            "sql_query": "SELECT city, COUNT(*) as customer_count FROM customers GROUP BY city ORDER BY customer_count DESC;"
        },
        {
            "question": "Find expensive products over $500",
            "sql_query": "SELECT * FROM products WHERE price > 500;"
        }
    ]

def create_comprehensive_training_data():
    """Create comprehensive training data combining all sources"""
    training_data = []
    
    # Add CSV questions with template answers
    csv_questions = get_sample_csv_questions()
    for question in csv_questions:
        answer = "I'll analyze the CSV data to answer your question."
        if "total" in question.lower() or "sum" in question.lower():
            answer = "Let me calculate the total from the CSV data."
        elif "average" in question.lower() or "mean" in question.lower():
            answer = "I'll compute the average from the CSV data."
        elif "distribution" in question.lower():
            answer = "I'll analyze the distribution in the CSV data."
        elif "correlation" in question.lower():
            answer = "I'll examine the correlations in the CSV data."
        elif "top" in question.lower() or "highest" in question.lower():
            answer = "I'll find the top results from the CSV data."
        
        training_data.append({
            "question": question,
            "answer": answer
        })
    
    # Add SQL questions
    sql_questions = get_additional_sql_questions()
    for sql_qa in sql_questions:
        training_data.append({
            "question": sql_qa["question"],
            "answer": f"Here's the SQL query to answer your question: {sql_qa['sql_query']}"
        })
    
    # Add general chatbot responses
    general_qa = [
        {
            "question": "What can you help me with?",
            "answer": "I can help you analyze database schemas, write SQL queries, and analyze CSV data. You can ask me about data summaries, statistics, correlations, and more!"
        },
        {
            "question": "How do I use this chatbot?",
            "answer": "Simply ask me questions about your database or CSV data! I can generate SQL queries, analyze data patterns, and provide insights from your datasets."
        },
        {
            "question": "What types of data analysis can you perform?",
            "answer": "I can perform various analyses including: calculating averages and sums, finding correlations, generating distributions, identifying top performers, and creating SQL queries for complex data retrieval."
        }
    ]
    
    training_data.extend(general_qa)
    
    return training_data
