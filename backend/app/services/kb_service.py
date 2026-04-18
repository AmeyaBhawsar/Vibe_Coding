from app.data.mock_db import db

class KnowledgeBaseService:
    @staticmethod
    def search(query: str) -> str | None:
        """
        30-Second Swap Test: Replace this logic with an OpenAI API call 
        if you want to transition to a real LLM in the future.
        """
        lower_query = query.lower()
        
        # Find best matching article based on keywords
        for article in db["kb"]:
            if any(kw in lower_query for kw in article["keywords"]):
                return article["resolution_steps"]
                
        return None