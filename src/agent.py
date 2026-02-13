from planner import QueryPlanner
from retriever import ArxivRetriever
from models.embeddings import EmbeddingModel
from utils.vector_store import VectorStore
from utils.chunking import chunk_text
from summarizer import ResearchSummarizer
from utils.logging import get_logger
import uuid

logger = get_logger("Agent")


def run(query: str):
    logger.info("Starting research agent")

    # 1. Plan
    yield {"type": "status", "message": "Planning research strategy..."}
    planner = QueryPlanner()
    plan = planner.plan(query)
    logger.info(f"plan ---------{plan}")
    search_query = plan.get("search_queries", query)
    logger.info(f"search_query-------------{search_query}")

    # 2. Retrieve
    yield {"type": "status", "message": "Fetching academic papers..."}
    retriever = ArxivRetriever(max_results=20)
    papers = retriever.fetch(search_query)

    if not papers:
        logger.warning("No papers retrieved")
        yield {"type": "status", "message": "No papers found."}
        return

    # 3. Chunk + Embed
    yield {"type": "status", "message": "Chunking and embedding papers..."}
    embedder = EmbeddingModel()
    vector_store = VectorStore()

    chunk_texts = []
    metadatas = []
    ids = []

    for paper in papers:
        chunks = chunk_text(paper["summary"])

        for chunk in chunks:
            chunk_texts.append(chunk)
            metadatas.append(
                {
                    "title": paper["title"],
                    "authors": ", ".join(paper["authors"]),
                    "link": paper["link"],
                    "source": paper["source"],
                }
            )
            ids.append(str(uuid.uuid4()))

    embeddings = embedder.embed(chunk_texts)
    vector_store.add(ids, embeddings, chunk_texts, metadatas)

    # 4. Semantic Retrieval
    yield {"type": "status", "message": "Retrieving relevant research sections..."}
    query_embedding = embedder.embed([query])[0]
    results = vector_store.query(query_embedding, top_k=8)

    top_chunks = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        top_chunks.append(
            {
                "text": text,
                "title": meta["title"],
                "link": meta["link"],
            }
        )

    # 5. Summarize
    summarizer = ResearchSummarizer()
    # report = summarizer.summarize(query, top_chunks)


    for token in summarizer.summarize(query, top_chunks):
        yield {"type": "token", "content": token}




if __name__ == "__main__":
    run("Heart disease")



