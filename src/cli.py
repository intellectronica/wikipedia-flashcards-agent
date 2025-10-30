#!/usr/bin/env python3
"""
Wikipedia Flashcards Generator CLI

Step 1 implementation: Wikipedia search only.
Takes a topic as command-line arguments and searches Wikipedia for relevant articles.
"""

import sys
import logging

from src.agents.wikipedia_search import search_wikipedia_articles

# Configure logging to be verbose
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


def main():
    """
    Main CLI entrypoint.
    
    Step 1 behavior:
    - Parse command-line arguments as the search query
    - Run Wikipedia search agent (Agent 1)
    - Log results and article details
    """
    # Parse command-line arguments into a query string
    if len(sys.argv) < 2:
        logger.error("Usage: uv run src/cli.py <topic>")
        logger.error("Example: uv run src/cli.py Quantum computing")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    logger.info("=" * 80)
    logger.info("Wikipedia Flashcards Generator - Step 1")
    logger.info(f"Query: '{query}'")
    logger.info("=" * 80)
    
    try:
        # Run Agent 1: Wikipedia Search
        logger.info("Starting Wikipedia search...")
        result = search_wikipedia_articles(query)
        
        # Log results
        logger.info(f"\n{'=' * 80}")
        logger.info(f"RESULTS: Found {len(result.articles)} articles")
        logger.info(f"{'=' * 80}")
        
        for i, article in enumerate(result.articles, 1):
            logger.info(f"\nArticle {i}: {article.title}")
            logger.info(f"  Content length: {len(article.content):,} characters")
            logger.info(f"  First 200 chars: {article.content[:200]}...")
        
        logger.info(f"\n{'=' * 80}")
        logger.info("Step 1 completed successfully!")
        logger.info(f"Total articles: {len(result.articles)}")
        total_chars = sum(len(a.content) for a in result.articles)
        logger.info(f"Total content: {total_chars:,} characters")
        logger.info("=" * 80)
        
    except ValueError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
