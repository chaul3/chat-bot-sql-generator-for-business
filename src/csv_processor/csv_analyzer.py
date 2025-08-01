"""
CSV analyzer for processing and analyzing CSV files for business questions
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional
import io

class CSVAnalyzer:
    def __init__(self):
        """Initialize CSV analyzer"""
        self.df = None
        self.file_info = {}
        
    def load_csv(self, file_path_or_buffer, **kwargs) -> bool:
        """
        Load CSV file into pandas DataFrame
        
        Args:
            file_path_or_buffer: File path, URL, or file-like object
            **kwargs: Additional arguments for pandas.read_csv
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            self.df = pd.read_csv(file_path_or_buffer, **kwargs)
            self.file_info = {
                "shape": self.df.shape,
                "columns": list(self.df.columns),
                "dtypes": self.df.dtypes.to_dict(),
                "memory_usage": self.df.memory_usage(deep=True).sum(),
                "null_counts": self.df.isnull().sum().to_dict()
            }
            return True
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return False
    
    def has_data(self) -> bool:
        """Check if CSV data is loaded"""
        return self.df is not None and not self.df.empty
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of the CSV data"""
        if not self.has_data():
            return {"error": "No data loaded"}
        
        summary = {
            "basic_info": self.file_info,
            "numerical_summary": self._get_numerical_summary(),
            "categorical_summary": self._get_categorical_summary(),
            "missing_data": self._get_missing_data_info(),
            "sample_data": self.df.head().to_dict('records')
        }
        
        return summary
    
    def _get_numerical_summary(self) -> Dict[str, Any]:
        """Get summary statistics for numerical columns"""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) == 0:
            return {"message": "No numerical columns found"}
        
        return {
            "columns": list(numerical_cols),
            "statistics": self.df[numerical_cols].describe().to_dict(),
            "correlations": self.df[numerical_cols].corr().to_dict() if len(numerical_cols) > 1 else {}
        }
    
    def _get_categorical_summary(self) -> Dict[str, Any]:
        """Get summary for categorical columns"""
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) == 0:
            return {"message": "No categorical columns found"}
        
        summary = {}
        for col in categorical_cols:
            summary[col] = {
                "unique_count": self.df[col].nunique(),
                "most_common": self.df[col].value_counts().head().to_dict(),
                "sample_values": self.df[col].dropna().unique()[:10].tolist()
            }
        
        return summary
    
    def _get_missing_data_info(self) -> Dict[str, Any]:
        """Get information about missing data"""
        missing_counts = self.df.isnull().sum()
        missing_percentages = (missing_counts / len(self.df)) * 100
        
        return {
            "total_missing": int(missing_counts.sum()),
            "missing_by_column": missing_counts[missing_counts > 0].to_dict(),
            "missing_percentages": missing_percentages[missing_percentages > 0].to_dict()
        }
    
    def get_column_names(self) -> List[str]:
        """Get list of column names"""
        if not self.has_data():
            return []
        return list(self.df.columns)
    
    def analyze_question(self, question: str) -> str:
        """
        Analyze CSV data based on a natural language question
        
        Args:
            question: Natural language question about the data
            
        Returns:
            Analysis result as a string
        """
        if not self.has_data():
            return "No CSV data loaded. Please upload a CSV file first."
        
        question_lower = question.lower()
        
        try:
            # Handle different types of questions
            if any(word in question_lower for word in ['average', 'mean']):
                return self._handle_average_question(question)
            elif any(word in question_lower for word in ['sum', 'total']):
                return self._handle_sum_question(question)
            elif any(word in question_lower for word in ['count', 'how many']):
                return self._handle_count_question(question)
            elif any(word in question_lower for word in ['max', 'maximum', 'highest']):
                return self._handle_max_question(question)
            elif any(word in question_lower for word in ['min', 'minimum', 'lowest']):
                return self._handle_min_question(question)
            elif any(word in question_lower for word in ['correlation', 'relationship']):
                return self._handle_correlation_question(question)
            elif any(word in question_lower for word in ['distribution', 'spread']):
                return self._handle_distribution_question(question)
            elif any(word in question_lower for word in ['columns', 'fields']):
                return f"Columns in the dataset: {', '.join(self.df.columns)}"
            elif any(word in question_lower for word in ['shape', 'size', 'dimensions']):
                return f"Dataset shape: {self.df.shape[0]} rows, {self.df.shape[1]} columns"
            elif 'summary' in question_lower or 'overview' in question_lower:
                return self._get_overview_text()
            else:
                return self._handle_general_question(question)
                
        except Exception as e:
            return f"Error analyzing question: {str(e)}"
    
    def _handle_average_question(self, question: str) -> str:
        """Handle questions about averages"""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Try to find column mentioned in question
        mentioned_col = None
        for col in self.df.columns:
            if col.lower() in question.lower():
                mentioned_col = col
                break
        
        if mentioned_col and mentioned_col in numerical_cols:
            avg_value = self.df[mentioned_col].mean()
            return f"Average {mentioned_col}: {avg_value:.2f}"
        elif len(numerical_cols) > 0:
            averages = []
            for col in numerical_cols:
                avg = self.df[col].mean()
                averages.append(f"{col}: {avg:.2f}")
            return "Averages:\n" + "\n".join(averages)
        else:
            return "No numerical columns found for calculating averages."
    
    def _handle_sum_question(self, question: str) -> str:
        """Handle questions about sums/totals"""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        
        mentioned_col = None
        for col in self.df.columns:
            if col.lower() in question.lower():
                mentioned_col = col
                break
        
        if mentioned_col and mentioned_col in numerical_cols:
            total = self.df[mentioned_col].sum()
            return f"Total {mentioned_col}: {total:.2f}"
        elif len(numerical_cols) > 0:
            totals = []
            for col in numerical_cols:
                total = self.df[col].sum()
                totals.append(f"{col}: {total:.2f}")
            return "Totals:\n" + "\n".join(totals)
        else:
            return "No numerical columns found for calculating totals."
    
    def _handle_count_question(self, question: str) -> str:
        """Handle questions about counts"""
        mentioned_col = None
        for col in self.df.columns:
            if col.lower() in question.lower():
                mentioned_col = col
                break
        
        if mentioned_col:
            if self.df[mentioned_col].dtype == 'object':
                value_counts = self.df[mentioned_col].value_counts()
                return f"Value counts for {mentioned_col}:\n{value_counts.to_string()}"
            else:
                non_null_count = self.df[mentioned_col].count()
                return f"Non-null count for {mentioned_col}: {non_null_count}"
        else:
            return f"Total number of rows: {len(self.df)}"
    
    def _handle_max_question(self, question: str) -> str:
        """Handle questions about maximum values"""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        
        mentioned_col = None
        for col in self.df.columns:
            if col.lower() in question.lower():
                mentioned_col = col
                break
        
        if mentioned_col and mentioned_col in numerical_cols:
            max_value = self.df[mentioned_col].max()
            return f"Maximum {mentioned_col}: {max_value}"
        elif len(numerical_cols) > 0:
            maxes = []
            for col in numerical_cols:
                max_val = self.df[col].max()
                maxes.append(f"{col}: {max_val}")
            return "Maximum values:\n" + "\n".join(maxes)
        else:
            return "No numerical columns found for finding maximum values."
    
    def _handle_min_question(self, question: str) -> str:
        """Handle questions about minimum values"""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        
        mentioned_col = None
        for col in self.df.columns:
            if col.lower() in question.lower():
                mentioned_col = col
                break
        
        if mentioned_col and mentioned_col in numerical_cols:
            min_value = self.df[mentioned_col].min()
            return f"Minimum {mentioned_col}: {min_value}"
        elif len(numerical_cols) > 0:
            mins = []
            for col in numerical_cols:
                min_val = self.df[col].min()
                mins.append(f"{col}: {min_val}")
            return "Minimum values:\n" + "\n".join(mins)
        else:
            return "No numerical columns found for finding minimum values."
    
    def _handle_correlation_question(self, question: str) -> str:
        """Handle questions about correlations"""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_cols) < 2:
            return "Need at least 2 numerical columns to calculate correlations."
        
        corr_matrix = self.df[numerical_cols].corr()
        
        # Find strongest correlations
        correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                col1, col2 = corr_matrix.columns[i], corr_matrix.columns[j]
                corr_value = corr_matrix.iloc[i, j]
                correlations.append((abs(corr_value), col1, col2, corr_value))
        
        correlations.sort(reverse=True)
        
        result = "Strongest correlations:\n"
        for _, col1, col2, corr_val in correlations[:5]:
            result += f"{col1} - {col2}: {corr_val:.3f}\n"
        
        return result
    
    def _handle_distribution_question(self, question: str) -> str:
        """Handle questions about distributions"""
        mentioned_col = None
        for col in self.df.columns:
            if col.lower() in question.lower():
                mentioned_col = col
                break
        
        if mentioned_col:
            if self.df[mentioned_col].dtype in ['object', 'category']:
                value_counts = self.df[mentioned_col].value_counts()
                return f"Distribution of {mentioned_col}:\n{value_counts.to_string()}"
            else:
                stats = self.df[mentioned_col].describe()
                return f"Distribution statistics for {mentioned_col}:\n{stats.to_string()}"
        else:
            return "Please specify which column's distribution you'd like to see."
    
    def _handle_general_question(self, question: str) -> str:
        """Handle general questions"""
        return f"I understand you're asking about: '{question}'\n\n" + self._get_overview_text()
    
    def _get_overview_text(self) -> str:
        """Get a text overview of the dataset"""
        overview = f"""Dataset Overview:
- Shape: {self.df.shape[0]} rows, {self.df.shape[1]} columns
- Columns: {', '.join(self.df.columns)}
- Numerical columns: {len(self.df.select_dtypes(include=[np.number]).columns)}
- Categorical columns: {len(self.df.select_dtypes(include=['object', 'category']).columns)}
- Missing values: {self.df.isnull().sum().sum()} total"""
        
        return overview
    
    def generate_chart(self, question: str) -> Dict[str, Any]:
        """Generate chart data based on question"""
        if not self.has_data():
            return {"error": "No data loaded"}
        
        question_lower = question.lower()
        
        try:
            if 'histogram' in question_lower or 'distribution' in question_lower:
                return self._create_histogram_data()
            elif 'scatter' in question_lower or 'correlation' in question_lower:
                return self._create_scatter_data()
            elif 'bar' in question_lower or 'count' in question_lower:
                return self._create_bar_data()
            else:
                return self._create_default_chart_data()
        except Exception as e:
            return {"error": f"Error generating chart: {e}"}
    
    def _create_histogram_data(self) -> Dict[str, Any]:
        """Create histogram data for numerical columns"""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) == 0:
            return {"error": "No numerical columns for histogram"}
        
        col = numerical_cols[0]  # Use first numerical column
        return {
            "type": "histogram",
            "data": self.df[col].tolist(),
            "column": col,
            "title": f"Distribution of {col}"
        }
    
    def _create_scatter_data(self) -> Dict[str, Any]:
        """Create scatter plot data"""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) < 2:
            return {"error": "Need at least 2 numerical columns for scatter plot"}
        
        x_col, y_col = numerical_cols[0], numerical_cols[1]
        return {
            "type": "scatter",
            "x": self.df[x_col].tolist(),
            "y": self.df[y_col].tolist(),
            "x_column": x_col,
            "y_column": y_col,
            "title": f"{y_col} vs {x_col}"
        }
    
    def _create_bar_data(self) -> Dict[str, Any]:
        """Create bar chart data for categorical columns"""
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) == 0:
            return {"error": "No categorical columns for bar chart"}
        
        col = categorical_cols[0]
        value_counts = self.df[col].value_counts().head(10)
        
        return {
            "type": "bar",
            "labels": value_counts.index.tolist(),
            "values": value_counts.values.tolist(),
            "column": col,
            "title": f"Top values in {col}"
        }
    
    def _create_default_chart_data(self) -> Dict[str, Any]:
        """Create default chart based on data types"""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            return self._create_histogram_data()
        else:
            return self._create_bar_data()
    
    def get_business_insights(self) -> List[str]:
        """Generate business insights from the data"""
        insights = []
        
        if not self.has_data():
            return ["No data available for analysis"]
        
        # Data quality insights
        missing_pct = (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        if missing_pct > 10:
            insights.append(f"Data quality concern: {missing_pct:.1f}% missing values")
        
        # Size insights
        insights.append(f"Dataset contains {len(self.df):,} records with {len(self.df.columns)} attributes")
        
        # Numerical insights
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if self.df[col].std() > 0:  # Has variation
                insights.append(f"{col}: Range from {self.df[col].min():.2f} to {self.df[col].max():.2f}")
        
        # Categorical insights
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            unique_count = self.df[col].nunique()
            if unique_count < len(self.df) * 0.8:  # Not mostly unique
                insights.append(f"{col}: {unique_count} unique values, most common is '{self.df[col].mode()[0]}'")
        
        return insights
