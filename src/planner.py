from groq import Groq
from utils.logging import get_logger
import json
import os
from dotenv import load_dotenv
from models.llms import GroqModel


logger = get_logger("Planner")


class QueryPlanner:
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        load_dotenv()
        groqmodel = GroqModel(model)
        self.client = groqmodel.client
        self.model = groqmodel.model



    def plan(self, query: str) -> dict:
        logger.info(f"Planning search strategy for query: {query}")

        prompt = f"""
You are a research query normalization engine.
Your task is to extract the core research topic from a user’s natural language input
and convert it into a concise, academic-style search query.

Rules:
- Ignore conversational phrases (e.g., "I want to research", "can you help me", "tell me about")
- Identify the main research concept only
- Do NOT add new concepts
- Keep the refined query short and search-friendly
- Do NOT use markdown or code fences

Return a JSON object with EXACTLY these keys:
- refined_query: a short academic-style topic (string)
- keywords: a list of important domain keywords (array of strings)

Example:

User input:
"I want to research about heart disease"

Output:
{{
  "refined_query": "heart disease",
  "keywords": ["heart disease", "cardiovascular disease"]
}}

Return valid JSON only.
No explanations.
No markdown.

User input:
"{query}"
"""


        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        try:
            plan = json.loads(content)
        except json.JSONDecodeError:
            logger.error("Planner returned invalid JSON")
            plan = {
                "refined_query": query,
                "keywords": query.split()
            }

        return plan

