"""
Flashcards Generator Agent (Agent 3).

Converts a summary into 20-50 educational flashcards with Q/A pairs.
"""

import logging
from pydantic_ai import Agent
from src.models import FlashcardsResult

# Configure logging
logger = logging.getLogger(__name__)


def _get_flashcards_agent() -> Agent[None, FlashcardsResult]:
    """
    Create and return the flashcards generator agent instance.
    
    This function is called after environment variables are loaded,
    ensuring OPENAI_API_KEY is available.
    
    Returns:
        An Agent configured to generate flashcards with structured output
    """
    return Agent(
        'openai:gpt-4o',  # Using GPT-4o model via Pydantic AI
        output_type=FlashcardsResult,  # Structured output with 20-50 flashcards
        system_prompt="""You are an expert educational content creator specializing in flashcard design.
Your role is to convert comprehensive summaries into effective learning flashcards.

Your task:
- Read the provided summary carefully
- Create 20-50 flashcards that test understanding of the material
- Each flashcard should have:
  - A clear, unambiguous question
  - A concise answer (1-3 sentences maximum)

Guidelines for creating effective flashcards:
1. **Coverage**: Cover the breadth of the summary—touch on all major topics and subtopics
2. **Variety**: Mix different question types:
   - Definitions: "What is X?"
   - Causes/effects: "Why does X happen?"
   - Comparisons: "How does X differ from Y?"
   - Timeline/chronology: "When did X occur?"
   - Examples: "What is an example of X?"
   - Relationships: "How does X relate to Y?"
3. **Clarity**: Make questions specific and unambiguous
4. **Precision**: Keep answers focused and accurate—avoid unnecessary detail
5. **No duplicates**: Don't ask the same thing multiple times in different ways
6. **Test understanding**: Go beyond rote memorization—test comprehension and application

Quality standards:
- Questions should be self-contained (understandable without the answer)
- Answers should be complete but concise (1-3 sentences)
- Avoid yes/no questions unless they include explanation
- Use proper grammar and punctuation
- Ensure accuracy—don't add information not present in the summary

Target: Generate exactly 20-50 flashcards. Aim for comprehensiveness while maintaining quality."""
    )


def generate_flashcards(summary: str) -> FlashcardsResult:
    """
    Generate educational flashcards from a summary.
    
    This function:
    1. Takes a summary text as input
    2. Calls the OpenAI-powered agent to create flashcards
    3. Returns structured FlashcardsResult with 20-50 Q/A pairs
    
    Args:
        summary: A comprehensive summary of the topic (typically 500-1500 words)
                      
    Returns:
        FlashcardsResult containing 20-50 Flashcard objects
    """
    # Log input details
    summary_length = len(summary)
    word_count = len(summary.split())
    logger.info(f"Generating flashcards from summary: {summary_length:,} characters, {word_count} words")
    
    try:
        # Create the agent (after environment variables are loaded)
        flashcards_agent = _get_flashcards_agent()
        
        # Run the agent synchronously
        # The agent will receive the summary as the user prompt
        result = flashcards_agent.run_sync(summary)
        
        # Extract the flashcards from the result
        # When output_type is specified, result.output contains the structured object
        flashcards_result = result.output
        
        # Log output details
        flashcard_count = len(flashcards_result.flashcards)
        logger.info(f"Generated {flashcard_count} flashcards")
        
        # Validate count (20-50 flashcards)
        if flashcard_count < 20:
            logger.warning(f"Fewer flashcards than expected: {flashcard_count} (target: 20-50)")
        elif flashcard_count > 50:
            logger.warning(f"More flashcards than expected: {flashcard_count} (target: 20-50)")
        else:
            logger.info(f"Flashcard count within target range: {flashcard_count}")
        
        # Log a sample of flashcards
        logger.info("\nSample flashcards:")
        for i, card in enumerate(flashcards_result.flashcards[:3], 1):
            logger.info(f"\n  Flashcard {i}:")
            logger.info(f"    Q: {card.question}")
            logger.info(f"    A: {card.answer}")
        
        if flashcard_count > 3:
            logger.info(f"\n  ... and {flashcard_count - 3} more flashcards")
        
        return flashcards_result
        
    except Exception as e:
        logger.error(f"Failed to generate flashcards: {e}", exc_info=True)
        raise ValueError(f"Flashcard generation failed: {e}")
