import requests
from typing import List, Dict
from utils.logging import get_logger
import os
from dotenv import load_dotenv
load_dotenv()

logger = get_logger("Retriever")

ARXIV_API_URL = os.getenv("ARXIV_API_URL")
if not ARXIV_API_URL:
    raise RuntimeError("ARXIV_API_URL not set")


class ArxivRetriever:
    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    def fetch(self, query: str) -> List[Dict]:
        logger.info(f"Fetching papers from arXiv for query: {query}")

        # params = {
        #     "search_query": f"all:{query}",
        #     "start": 0,
        #     "max_results": self.max_results,
        #     "sortBy": "submittedDate",
        #     "sortOrder": "descending",
        # }

        params = {
            "search_query": f'ti:"{query}" OR abs:"{query}"',
            "start": 0,
            "max_results": self.max_results,
            "sortBy": "relevance",
        }
#         headers = {
#     "User-Agent": "ResearchAssistantAgent/1.0 (contact: jj@gmail.com)"
# }

        # response = requests.get(ARXIV_API_URL, params=params, headers=headers, timeout=10)



        response = requests.get(ARXIV_API_URL, params=params, timeout=10)
        response.raise_for_status()

        return self._parse_response(response.text)


    def _parse_response(self, raw_xml: str) -> List[Dict]:
        import feedparser

        feed = feedparser.parse(raw_xml)
        papers = []

        for entry in feed.entries:
            papers.append(
                {
                    "title": entry.title,
                    "authors": [author.name for author in entry.authors],
                    "summary": entry.summary,
                    "published": entry.published,
                    "link": entry.link,
                    "source": "arXiv",
                }
            )
            logger.info(f"Retrieved {entry.title} paper from arXiv")

        logger.info(f"Retrieved {len(papers)} papers from arXiv")
        return papers
