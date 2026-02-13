import os
from groq import Groq
from dotenv import load_dotenv
from utils.logging import get_logger

logger = get_logger("Summarizer")


class ResearchSummarizer:
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        load_dotenv()

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)
        self.model = model

    def summarize(self, query: str, chunks: list[dict]):
        """
        chunks: list of dicts with keys:
        - text
        - title
        - link
        """

        logger.info("Synthesizing research summary")

        context = ""
        for c in chunks:
            context += f"""
Paper: {c['title']}
Content: {c['text']}
Source: {c['link']}
"""

        prompt = f"""
You are a professional research assistant.

Using the provided research excerpts, generate a concise, structured research report
for the topic:

"{query}"

The report MUST have the following sections:

1. Overview (short synthesis, not a list)
2. Key Techniques / Approaches
3. Major Trends
4. Open Challenges / Gaps
5. References (titles with links)

Rules:
- Do NOT summarize papers one by one
- Synthesize across all sources
- Be factual and neutral
- Use clear, professional language

Research excerpts:
{context}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            stream=True
        )

        # return response.choices[0].message.content
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
