"""
Analysis & Summary Agent (Agent 2).

Synthesizes multiple Wikipedia articles into a coherent 500-1500 word summary.
"""

import logging
from pydantic_ai import Agent

# Configure logging
logger = logging.getLogger(__name__)

# Define the summary agent with OpenAI GPT-4o
# This agent takes combined article text and produces a plain string summary
summary_agent = Agent(
    'openai:gpt-4o',  # Using GPT-4o model via Pydantic AI
    # No output_type specified = returns plain string
    system_prompt="""You are an expert educational content synthesizer. Your role is to analyze 
multiple Wikipedia articles and create a comprehensive, coherent summary for learning purposes.

Your task:
- Read the provided Wikipedia articles (they will be separated with headers and dividers)
- Synthesize the information into a single, well-structured narrative
- Output should be 500-1500 words in length
- Cover key facts, definitions, relationships, and chronology where applicable
- Include notable controversies or open questions if relevant
- Write in a clear, readable style suitable for educational flashcards
- Avoid bullet points unless necessary—aim for flowing, coherent paragraphs
- Be comprehensive but concise—capture the essential information

The summary will be used to generate educational flashcards, so ensure you cover:
- Core concepts and definitions
- Important relationships and connections
- Key historical developments or timeline events
- Notable examples or applications
- Contrasting viewpoints or debates (if any)

Write as a domain expert explaining the topic to an interested learner."""
)


def generate_summary(articles_text: str) -> str:
    """
    Generate a comprehensive summary from combined Wikipedia articles.
    
    This function:
    1. Takes concatenated article text as input
    2. Calls the OpenAI-powered agent to synthesize the content
    3. Returns a 500-1500 word summary suitable for flashcard generation
    
    Args:
        articles_text: Combined text of all Wikipedia articles, formatted with
                      headers and separators
                      
    Returns:
        A coherent summary string (500-1500 words)
    """
    # Log input details
    input_length = len(articles_text)
    approx_tokens = input_length // 4  # Rough estimate: 1 token ≈ 4 characters
    logger.info(f"Generating summary from {input_length:,} characters (~{approx_tokens:,} tokens)")
    
    try:
        # Run the agent synchronously
        # The agent will receive the articles_text as the user prompt
        result = summary_agent.run_sync(articles_text)
        
        # Extract the summary from the result
        # When no output_type is specified, result.output contains the string
        summary = result.output
        
        # Log output details
        summary_length = len(summary)
        word_count = len(summary.split())
        logger.info(f"Generated summary: {summary_length:,} characters, {word_count} words")
        
        # Validate word count (500-1500 words)
        if word_count < 500:
            logger.warning(f"Summary is shorter than expected: {word_count} words (target: 500-1500)")
        elif word_count > 1500:
            logger.warning(f"Summary is longer than expected: {word_count} words (target: 500-1500)")
        else:
            logger.info(f"Summary word count within target range: {word_count} words")
        
        # Log a preview of the summary
        preview = summary[:300] + "..." if len(summary) > 300 else summary
        logger.info(f"Summary preview: {preview}")
        
        return summary
        
    except Exception as e:
        logger.error(f"Failed to generate summary: {e}", exc_info=True)
        raise
