"""
Pydantic models for Wikipedia flashcards generator.

These models define the data contracts between agents in the pipeline.
"""

from pydantic import BaseModel, Field


class WikipediaArticle(BaseModel):
    """
    Represents a single Wikipedia article with its title and full content.
    """
    title: str = Field(description="The canonical title of the Wikipedia article")
    content: str = Field(description="The full text content of the article (plain text, not HTML)")


class WikipediaSearchResult(BaseModel):
    """
    The output of the Wikipedia search agent.
    Contains 2-3 relevant articles found for the user's query.
    """
    articles: list[WikipediaArticle] = Field(
        description="List of 2-3 relevant Wikipedia articles with full content",
        min_length=2,
        max_length=3
    )


class Flashcard(BaseModel):
    """
    A single flashcard with a question and answer pair.
    """
    question: str = Field(description="The question to ask")
    answer: str = Field(description="The answer (1-3 sentences max)")


class FlashcardsResult(BaseModel):
    """
    The output of the flashcards generator agent.
    Contains 20-50 flashcards covering the summary content.
    """
    flashcards: list[Flashcard] = Field(
        description="List of 20-50 flashcards with Q/A pairs",
        min_length=20,
        max_length=50
    )
