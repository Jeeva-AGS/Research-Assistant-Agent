import requests
from typing import List, Dict
from utils.logging import get_logger

logger = get_logger("Retriever")

ARXIV_API_URL = "http://export.arxiv.org/api/query"


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


# if __name__ == "__main__":
#     retriever = ArxivRetriever(max_results=3)
#     results = retriever.fetch("Football Rules and Regulations")

#     for paper in results:
#         print(paper["title"])
