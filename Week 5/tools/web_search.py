from typing import List, Dict, Any
from langchain_core.tools import tool
from ddgs import DDGS
from config import get_azure_model, Config


class WebSearchTool:
    """Tool for searching the web using DuckDuckGo"""

    def __init__(self):
        self.llm = get_azure_model()
        self.ddgs = DDGS()

    def _search_web(self, query: str, max_results: int = None) -> List[Dict[str, Any]]:
        """Perform web search using DuckDuckGo"""
        if max_results is None:
            max_results = Config.MAX_SEARCH_RESULTS

        try:
            results = []
            search_results = self.ddgs.text(query, max_results=max_results)

            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'body': result.get('body', ''),
                    'href': result.get('href', ''),
                })

            return results
        except Exception as e:
            return [{'error': f"Search failed: {str(e)}"}]

    def _analyze_search_results(self, results: List[Dict[str, Any]], query: str, context: str) -> str:
        """Use LLM to analyze and summarize search results"""
        if not results:
            return "No search results found."

        if len(results) == 1 and 'error' in results[0]:
            return results[0]['error']

        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"Result {i}:\n"
                f"Title: {result['title']}\n"
                f"Content: {result['body']}\n"
                f"URL: {result['href']}\n"
            )

        search_content = "\n---\n".join(formatted_results)

        try:
            response = self.llm.invoke([
                {
                    "role": "system",
                    "content": f"You are a helpful assistant analyzing web search results for {context} support queries. "
                    f"Extract and summarize the most relevant information that answers the user's question. "
                    f"Focus on practical, actionable information. If the results don't contain relevant information, say so clearly. "
                    f"Always include source URLs for important information."
                },
                {
                    "role": "user",
                    "content": f"Query: {query}\n\nSearch Results:\n{search_content}\n\n"
                    f"Please provide a helpful summary of the most relevant information from these search results."
                }
            ])
            return response.content
        except Exception as e:
            return f"Error analyzing search results: {str(e)}\n\nRaw results:\n{search_content[:1000]}..."


def create_web_search_tool(context: str, tool_name: str = "web_search"):
    """Create a WebSearch tool for a specific context (IT or Finance)"""

    searcher = WebSearchTool()

    @tool
    def web_search(query: str) -> str:
        """
        Search the web for information using DuckDuckGo.

        Args:
            query: The search query or question you want to find information about

        Returns:
            Summarized information from web search results with source URLs
        """
        try:
            if context.lower() == "it":
                enhanced_query = f"{query} IT support technical guide"
            elif context.lower() == "finance":
                enhanced_query = f"{query} finance business accounting guide"
            else:
                enhanced_query = query
            results = searcher._search_web(enhanced_query)

            summary = searcher._analyze_search_results(results, query, context)

            return summary

        except Exception as e:
            return f"Web search error: {str(e)}"

    web_search.name = tool_name
    return web_search


def create_it_web_search_tool():
    """Create a web search tool optimized for IT queries"""
    return create_web_search_tool("IT", "web_search_it")


def create_finance_web_search_tool():
    """Create a web search tool optimized for Finance queries"""
    return create_web_search_tool("Finance", "web_search_finance")
