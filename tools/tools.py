from langchain_tavily import TavilySearch # 매우 최적화된 검색 API


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    search = TavilySearch() # 객체 생성
    res = search.run(f"{name}")
    return res