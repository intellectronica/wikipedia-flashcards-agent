#!/usr/bin/env python3
"""
Wikipedia Flashcards Generator CLI

Complete implementation: Wikipedia search + summary generation + flashcards generation.
Takes a topic as command-line arguments, searches Wikipedia, generates a summary,
and creates flashcards saved to a Markdown file.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from src.agents.wikipedia_search import search_wikipedia_articles
from src.agents.summary import generate_summary
from src.agents.flashcards import generate_flashcards

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
    
    Complete pipeline behavior:
    - Parse command-line arguments as the search query
    - Load environment variables (.env file with OPENAI_API_KEY)
    - Run Wikipedia search agent (Agent 1)
    - Concatenate article texts with headers
    - Run summary agent (Agent 2) to generate 500-1500 word synthesis
    - Run flashcards agent (Agent 3) to create 20-50 Q/A pairs
    - Save flashcards to Markdown file in tmp/ directory
    - Log results at each stage
    """
    # Load environment variables from .env file
    load_dotenv()
    logger.info("Environment variables loaded from .env")
    
    # Parse command-line arguments into a query string
    if len(sys.argv) < 2:
        logger.error("Usage: uv run src/cli.py <topic>")
        logger.error("Example: uv run src/cli.py Quantum computing")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    logger.info("=" * 80)
    logger.info("Wikipedia Flashcards Generator - Complete Pipeline")
    logger.info(f"Query: '{query}'")
    logger.info("=" * 80)
    
    try:
        # ======================================================================
        # STEP 1: Wikipedia Search
        # ======================================================================
        logger.info("\n[STEP 1] Starting Wikipedia search...")
        result = search_wikipedia_articles(query)
        
        # Log Agent 1 results
        logger.info(f"\n{'=' * 80}")
        logger.info(f"[STEP 1 RESULTS] Found {len(result.articles)} articles")
        logger.info(f"{'=' * 80}")
        
        for i, article in enumerate(result.articles, 1):
            logger.info(f"\nArticle {i}: {article.title}")
            logger.info(f"  Content length: {len(article.content):,} characters")
            logger.info(f"  First 200 chars: {article.content[:200]}...")
        
        total_chars = sum(len(a.content) for a in result.articles)
        logger.info(f"\n[STEP 1 COMPLETE] Total content: {total_chars:,} characters")
        
        # ======================================================================
        # Concatenate articles for Agent 2
        # ======================================================================
        logger.info(f"\n{'=' * 80}")
        logger.info("[PREPARATION] Concatenating articles for summary generation...")
        logger.info(f"{'=' * 80}")
        
        # Format: # Title\n\nContent\n\n---\n\n
        combined_text = ""
        for article in result.articles:
            combined_text += f"# {article.title}\n\n"
            combined_text += f"{article.content}\n\n"
            combined_text += "---\n\n"
        
        combined_length = len(combined_text)
        logger.info(f"Combined text: {combined_length:,} characters")
        
        # ======================================================================
        # STEP 2: Generate Summary
        # ======================================================================
        logger.info(f"\n{'=' * 80}")
        logger.info("[STEP 2] Generating summary with OpenAI...")
        logger.info(f"{'=' * 80}")
        
        summary = generate_summary(combined_text)
        
        # Log Agent 2 results
        logger.info(f"\n{'=' * 80}")
        logger.info("[STEP 2 RESULTS] Summary generated successfully")
        logger.info(f"{'=' * 80}")
        logger.info(f"Summary length: {len(summary):,} characters")
        logger.info(f"Summary word count: {len(summary.split())} words")
        logger.info(f"\nSummary preview:\n{'-' * 80}\n{summary[:500]}...\n{'-' * 80}")
        
        # ======================================================================
        # STEP 3: Generate Flashcards
        # ======================================================================
        logger.info(f"\n{'=' * 80}")
        logger.info("[STEP 3] Generating flashcards with OpenAI...")
        logger.info(f"{'=' * 80}")
        
        flashcards_result = generate_flashcards(summary)
        
        # Log Agent 3 results
        logger.info(f"\n{'=' * 80}")
        logger.info("[STEP 3 RESULTS] Flashcards generated successfully")
        logger.info(f"{'=' * 80}")
        logger.info(f"Flashcard count: {len(flashcards_result.flashcards)}")
        
        # ======================================================================
        # Save flashcards to Markdown file
        # ======================================================================
        logger.info(f"\n{'=' * 80}")
        logger.info("[SAVING] Writing flashcards to Markdown file...")
        logger.info(f"{'=' * 80}")
        
        # Create slug from query (lowercase, replace spaces with hyphens, limit length)
        slug = query.lower().replace(" ", "-")[:50]
        
        # Generate timestamp (YYYYMMDD_HHMM format)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
        # Construct filename: flashcards_{slug}_{timestamp}.md
        filename = f"flashcards_{slug}_{timestamp}.md"
        
        # Ensure tmp/ directory exists
        tmp_dir = Path("tmp")
        tmp_dir.mkdir(exist_ok=True)
        
        # Full path to output file
        output_path = tmp_dir / filename
        
        # Render Markdown content
        markdown_content = f"""# Flashcards: {query}

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

"""
        
        # Add each flashcard with Q/A format
        for i, card in enumerate(flashcards_result.flashcards, 1):
            markdown_content += f"## Flashcard {i}\n\n"
            markdown_content += f"**Q:** {card.question}\n\n"
            markdown_content += f"**A:** {card.answer}\n\n"
            markdown_content += "---\n\n"
        
        # Write to file
        output_path.write_text(markdown_content, encoding="utf-8")
        
        # Log success with absolute path
        absolute_path = output_path.resolve()
        logger.info(f"Flashcards saved to: {absolute_path}")
        logger.info(f"File size: {len(markdown_content):,} characters")
        
        logger.info(f"\n{'=' * 80}")
        logger.info("Pipeline completed successfully!")
        logger.info(f"Generated {len(flashcards_result.flashcards)} flashcards from {len(result.articles)} Wikipedia articles")
        logger.info(f"Output: {absolute_path}")
        logger.info("=" * 80)
        
    except ValueError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
