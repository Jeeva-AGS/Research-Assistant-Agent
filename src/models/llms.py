import os
from groq import Groq
from dotenv import load_dotenv
from utils.logging import get_logger
load_dotenv()
logger = get_logger("LLMS")


class GroqModel:
    def __init__(self, model):   

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)
        self.model = model