from ddgs import DDGS

def web_search(query: str) -> str:
    """Search the web for current information on any topic and return top results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return f"No results found for: {query}"

        lines = []
        for r in results:
            title = r.get("title", "")
            body = r.get("body", "")[:150]
            lines.append(f"- {title}: {body}")

        return f"Top results for '{query}':\n" + "\n".join(lines)
    except Exception as e:
        return f"Error searching: {e}"

if __name__ == "__main__":
    print(web_search("latest AI news"))