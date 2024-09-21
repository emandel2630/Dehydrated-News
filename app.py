import asyncio
import os
from datetime import datetime

import aiohttp
import httpx
import openai
from dotenv import load_dotenv

# Updated import for ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

# Set your API keys
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "EMPTY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "EMPTY")
WORLD_NEWS_API_KEY = os.environ.get("WORLD_NEWS_API_KEY", "EMPTY")

if not NEWS_API_KEY or NEWS_API_KEY == "EMPTY":
    raise Exception(
        "Please set your NEWS_API_KEY environment variable or replace 'EMPTY' with your actual key."
    )
if not OPENAI_API_KEY or OPENAI_API_KEY == "EMPTY":
    raise Exception(
        "Please set your OPENAI_API_KEY environment variable or replace 'EMPTY' with your actual key."
    )
if not WORLD_NEWS_API_KEY or WORLD_NEWS_API_KEY == "EMPTY":
    raise Exception(
        "Please set your WORLD_NEWS_API_KEY environment variable or replace 'EMPTY' with your actual key."
    )

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY


class NewsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    async def fetch_news_articles(self, query=None, page=1):
        today = datetime.now().strftime("%Y-%m-%d")
        url = (
            "https://newsapi.org/v2/everything?"
            f"from={today}&"
            f"to={today}&"
            "language=en&"
            f"pageSize=20&"
            f"page={page}&"
            f"apiKey={self.api_key}"
        )

        if query:
            url += f"&q={query}"

        try:
            async with httpx.AsyncClient(http2=True) as client:
                response = await client.get(url)
                data = response.json()
                print(f"API Response: {data}")  # Debugging
                articles = data.get("articles", [])
                return articles
        except Exception as e:
            print(f"Error fetching news articles: {e}")
            return []

    async def fetch_all_articles(self, query=None, pages=1):
        tasks = [self.fetch_news_articles(query, page) for page in range(1, pages + 1)]
        articles = []
        for task in tasks:
            articles.extend(await task)
        return articles


class WorldNewsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    async def fetch_top_news(self):
        date = datetime.now().strftime("%Y-%m-%d")
        url = f"https://api.worldnewsapi.com/search-news?source-country=us&language=en&date={date}"
        headers = {"x-api-key": self.api_key}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(data)
                        return data.get("news", [])
                    else:
                        print(f"Error: {response.status}")
                        return []
        except Exception as e:
            print(f"Error fetching top news: {e}")
            return []


class FactExtractor:
    def __init__(self):
        self.cache = {}

    async def extract_facts(self, article_text):
        if article_text in self.cache:
            return self.cache[article_text]

        prompt_template = PromptTemplate(
            input_variables=["text"],
            template="""
Extract specific factual statements from the following text, including all relevant names of companies and people. 
Ensure that the facts are precise and contain specific details, without any narrative or value judgments.
Any predictions about future events based on the text should NOT be included. 
Any conjecture or speculation should NOT be included.
Do your best to carefully read the entire text before generating the facts so nothing is left out.
Present the facts as a numbered list.

Text:
{text}

Factual Statements:
""",
        )
        prompt = prompt_template.format(text=article_text)
        try:
            llm = ChatOpenAI(
                openai_api_key=openai.api_key, model_name="gpt-3.5-turbo", temperature=0
            )
            response = await llm.apredict(prompt)
            # Print the raw response for debugging
            print(f"Raw LLM Response:\n{response}\n")
            facts = [
                fact.strip("- ").strip()
                for fact in response.strip().split("\n")
                if fact.strip()
            ]
            self.cache[article_text] = facts
            return facts
        except Exception as e:
            print(f"Error extracting facts: {e}")
            return []


async def main():
    news_fetcher = NewsFetcher(NEWS_API_KEY)
    world_news_fetcher = WorldNewsFetcher(WORLD_NEWS_API_KEY)
    fact_extractor = FactExtractor()

    articles = []
    top_news_groups = []

    # Fetch articles with pagination
    query = "apple"
    pages = 2  # Number of pages to fetch
    articles = await news_fetcher.fetch_all_articles(query, pages)

    # Print the number of articles fetched
    print(f"Fetched {len(articles)} articles from NewsAPI.\n")

    # # Fetch top news from World News API
    # top_news_groups = await world_news_fetcher.fetch_top_news()
    # print(f"Fetched {len(top_news_groups)} top news groups from World News API.\n")

    # # Process all articles together
    with open("news_report.txt", "w", encoding="utf-8") as f:
        print(f"Processing all articles together.\n")
        f.write("News Report\n")
        f.write("=" * 50 + "\n\n")

        # Section for NewsAPI articles
        f.write("Section 1: NewsAPI Articles\n")
        f.write("-" * 50 + "\n\n")

        for article in articles:
            article_title = article.get("title", "No Title")
            article_url = article.get("url", "No URL")
            article_text = article.get("content") or article.get("description") or ""
            facts = await fact_extractor.extract_facts(article_text)
            # Write to file
            f.write(f"Title: {article_title}\n")
            f.write(f"URL: {article_url}\n")
            f.write("Facts:\n")
            for fact in facts:
                f.write(f"- {fact}\n")
            f.write("\n")
            # Print to console for debugging
            print(f"Title: {article_title}")
            print("Extracted Facts:")
            for fact in facts:
                print(f"- {fact}")
            print("\n")

        # Section for World News API top news
        f.write("Section 2: World News API Top News\n")
        f.write("-" * 50 + "\n\n")

        for news_item in top_news_groups:
            article_title = news_item.get("title", "No Title")
            article_url = news_item.get("url", "No URL")
            article_text = news_item.get("text") or news_item.get("summary") or ""
            facts = await fact_extractor.extract_facts(article_text)
            # Write to file
            f.write(f"Title: {article_title}\n")
            f.write(f"URL: {article_url}\n")
            f.write("Facts:\n")
            for fact in facts:
                f.write(f"- {fact}\n")
            f.write("\n")
            # Print to console for debugging
            print(f"Title: {article_title}")
            print("Extracted Facts:")
            for fact in facts:
                print(f"- {fact}")
            print("\n")
        f.write("\n")
    print("Text report generated as 'news_report.txt'.")


if __name__ == "__main__":
    asyncio.run(main())
