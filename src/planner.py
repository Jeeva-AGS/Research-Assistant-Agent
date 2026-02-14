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
You are a research assistant.

Given a user research query, return a JSON object with exactly these keys:
- refined_query (string)
- keywords (array of strings)

Do not include explanations.
Do not include markdown.
Return valid JSON only.

User query: "{query}"
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

