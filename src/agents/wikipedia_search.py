"""
Wikipedia Search Agent (Agent 1).

Searches Wikipedia for a topic, selects 2-3 relevant articles,
and fetches their full content.
"""

import logging
import wikipedia

from src.models import WikipediaArticle, WikipediaSearchResult

# Configure logging
logger = logging.getLogger(__name__)


def search_wikipedia_articles(query: str) -> WikipediaSearchResult:
    """
    Search Wikipedia for a topic and fetch full content of 2-3 relevant articles.
    
    This function:
    1. Searches Wikipedia for up to 10 candidate results
    2. Iterates through results to fetch the best 2-3 articles
    3. Handles disambiguation errors and page errors
    4. Returns articles with meaningful content (not stubs)
    
    Args:
        query: The search query/topic provided by the user
        
    Returns:
        WikipediaSearchResult containing 2-3 articles with full content
    """
    logger.info(f"Searching Wikipedia for query: '{query}'")
    
    # Search for candidate articles (up to 10 results)
    try:
        search_results = wikipedia.search(query, results=10)
        logger.info(f"Found {len(search_results)} candidate results: {search_results}")
    except Exception as e:
        logger.error(f"Wikipedia search failed: {e}")
        raise
    
    if not search_results:
        logger.warning("No search results found")
        raise ValueError(f"No Wikipedia articles found for query: '{query}'")
    
    # Fetch full content for the best 2-3 articles
    articles = []
    min_content_length = 500  # Minimum characters to avoid stub articles
    
    for result_title in search_results:
        # Stop once we have 3 good articles
        if len(articles) >= 3:
            break
        
        try:
            logger.debug(f"Attempting to fetch page: '{result_title}'")
            page = wikipedia.page(result_title, auto_suggest=False)
            
            # Extract content and check if it's substantial
            content = page.content
            if len(content) < min_content_length:
                logger.debug(f"Skipping '{page.title}' - content too short ({len(content)} chars)")
                continue
            
            # Filter out obvious non-article pages by title heuristics
            title_lower = page.title.lower()
            skip_keywords = ['list of', 'index of', 'portal:', 'category:']
            if any(keyword in title_lower for keyword in skip_keywords):
                logger.debug(f"Skipping '{page.title}' - appears to be a meta page")
                continue
            
            # Add the article
            article = WikipediaArticle(title=page.title, content=content)
            articles.append(article)
            logger.info(f"Added article: '{page.title}' ({len(content):,} characters)")
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation by trying the first option
            logger.debug(f"Disambiguation error for '{result_title}': {e.options[:3]}")
            if e.options:
                try:
                    first_option = e.options[0]
                    logger.debug(f"Trying first disambiguation option: '{first_option}'")
                    page = wikipedia.page(first_option, auto_suggest=False)
                    content = page.content
                    
                    if len(content) >= min_content_length:
                        article = WikipediaArticle(title=page.title, content=content)
                        articles.append(article)
                        logger.info(f"Added article (from disambiguation): '{page.title}' ({len(content):,} characters)")
                except Exception as inner_e:
                    logger.debug(f"Failed to fetch disambiguation option: {inner_e}")
                    continue
        
        except wikipedia.exceptions.PageError as e:
            logger.debug(f"Page not found: '{result_title}' - {e}")
            continue
        
        except Exception as e:
            logger.warning(f"Unexpected error fetching '{result_title}': {e}")
            continue
    
    # Ensure we have at least 2 articles
    if len(articles) < 2:
        logger.error(f"Only found {len(articles)} article(s), need at least 2")
        raise ValueError(
            f"Could not find enough substantial Wikipedia articles for '{query}'. "
            f"Found {len(articles)} article(s), need at least 2."
        )
    
    # Log summary
    total_chars = sum(len(article.content) for article in articles)
    logger.info(f"Successfully fetched {len(articles)} articles, total content: {total_chars:,} characters")
    
    return WikipediaSearchResult(articles=articles)
