"""
Question classifier to determine the type of user question
"""
import re

class QuestionClassifier:
    def __init__(self):
        """Initialize question classifier with keyword patterns"""
        self.patterns = {
            "database": [
                r"\b(sql|query|table|database|schema|select|insert|update|delete|join)\b",
                r"\b(show\s+tables|describe|explain)\b",
                r"\b(primary\s+key|foreign\s+key|index|constraint)\b"
            ],
            "csv": [
                r"\b(csv|data|dataset|file|average|mean|sum|total|count|distribution)\b",
                r"\b(columns?|rows?|records?|fields?)\b",
                r"\b(correlation|relationship|analysis|statistics)\b"
            ],
            "schema": [
                r"\b(schema|structure|tables?|columns?|fields?)\b",
                r"\b(what\s+(tables|columns|fields))\b",
                r"\b(show\s+me\s+the\s+structure)\b"
            ],
            "general": [
                r"\b(hello|hi|help|what|how|can\s+you)\b"
            ]
        }
    
    def classify(self, question: str) -> str:
        """
        Classify a question into one of the predefined categories
        
        Args:
            question: The user's question
            
        Returns:
            Classification category: 'database', 'csv', 'schema', or 'general'
        """
        question_lower = question.lower()
        
        # Score each category
        scores = {}
        for category, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, question_lower))
                score += matches
            scores[category] = score
        
        # Return category with highest score, default to 'general'
        if max(scores.values()) == 0:
            return "general"
        
        return max(scores, key=scores.get)
