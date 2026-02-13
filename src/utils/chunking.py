from typing import List
from utils.logging import get_logger

logger = get_logger("Chunking")


def chunk_text(text: str, max_length: int = 500) -> List[str]:
    """
    Chunk text by paragraphs with a max character limit.
    """
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) <= max_length:
            current_chunk += " " + para
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    logger.info(f"Created {len(chunks)} chunks")
    return chunks
