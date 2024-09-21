import asyncio
import os

import aiohttp
import openai
from dotenv import load_dotenv

# Updated import for ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

# Set your API keys
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not NEWS_API_KEY:
    raise Exception(
        "Please set your NEWS_API_KEY environment variable or replace 'YOUR_NEWSAPI_KEY' with your actual key."
    )
if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
    raise Exception(
        "Please set your OPENAI_API_KEY environment variable or replace 'YOUR_OPENAI_API_KEY' with your actual key."
    )

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY


class NewsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    async def fetch_news_article(self, query):
        url = (
            "https://newsapi.org/v2/everything?"
            f"q={query}&"
            "language=en&"
            "pageSize=1&"
            f"apiKey={self.api_key}"
        )
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    articles = data.get("articles", [])
                    if articles:
                        return articles[0]
                    else:
                        print("No articles found.")
                        return None
        except Exception as e:
            print(f"Error fetching news article: {e}")
            return None


class FactExtractor:
    async def extract_facts(self, article_text):
        # Updated prompt template for specificity
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
                openai_api_key=openai.api_key, model_name="gpt-4", temperature=0.5
            )
            response = await llm.apredict(prompt)
            # Extract facts from the response
            facts = [
                fact.strip("- ").strip()
                for fact in response.strip().split("\n")
                if fact.strip()
            ]
            return facts
        except Exception as e:
            print(f"Error extracting facts: {e}")
            return []


async def main():
    news_fetcher = NewsFetcher(NEWS_API_KEY)
    fact_extractor = FactExtractor()

    # Fetch a single article
    query = "latest news"
    # article = await news_fetcher.fetch_news_article(query)
    article = True

    if article:
        # article_title = article.get("title", "No Title")
        # article_url = article.get("url", "No URL")
        article_text = """
 The FBI and other federal authorities have boarded a vessel in Baltimore managed by the same company as the cargo ship that caused the collapse of the Francis Scott Key Bridge back in March.

Their visit comes just a few days after the Justice Department filed a lawsuit against the companies that owned and operated the deadly ship.

In an aerial view, a tug boat travels towards the Port of Baltimore as salvage crews continue to clean up wreckage from the collapse of the Francis Scott Key Bridge in the Patapsco River on June 11 in Baltimore. 
National
U.S. sues Dali ship owner and operator for $100 million over Baltimore bridge collapse
In a statement, the FBI said its agents along with officials from the U.S. Environmental Protection Agency’s Criminal Investigation Division and the Coast Guard's Investigative Services arrived at the Maersk Saltoro vessel Saturday morning.

The FBI said the group was "conducting court authorized law enforcement activity" and declined to provide more details.

Records from IHS Shipping Data show the Maersk Saltoro is managed by Synergy Marine Private Ltd., the same company that operated the cargo ship, Dali.

On March 26, the massive vessel lost power and crashed into the Baltimore bridge, killing six construction workers who had been repairing potholes in the overnight hours on the structure.

On Wednesday, the Justice Department announced it was suing Synergy Marine and the ship's owner, Grace Ocean Private Ltd., — both of which are Singapore-based corporations — for negligence and dangerous cost-cutting decisions that led to the bridge collapse.

The catastrophe shut down the busy port for months and it also obliterated a segment of Interstate 695 carried by the bridge.

“The ship’s owner and manager … sent an ill-prepared crew on an abjectly unseaworthy vessel to navigate the United States’ waterways,” the Justice Department said in a civil claim filed in a federal court in Maryland.

FBI agents are searching the ship that crashed into Baltimore's Key Bridge
Law
FBI agents are searching the ship that crashed into Baltimore's Key Bridge
The federal government is seeking more than $100 million in costs that the U.S. incurred in responding to the disaster. The federal claim does not cover the expenses of rebuilding the bridge. Since Maryland built and owned the bridge, the state will pursue its own compensation, according to the Justice Department.

The FBI has also opened a criminal investigation into the fatal collapse, with a focus on the massive ship and whether the crew knew that the vessel was malfunctioning before they left the port, the Washington Post reported in April.


        """
        print(article_text)
        # Extract facts
        facts = await fact_extractor.extract_facts(article_text)

        # Prepare the markdown content
        markdown_content = f"# Original Article\n\n"
        markdown_content += f"**Title:** FBI agents board Baltimore ship linked to Singaporean company sued in bridge collapse\n\n"
        markdown_content += f"**URL:** [Link to article](https://www.npr.org/2024/09/21/nx-s1-5121915/fbi-baltimore-bridge-collapse-cargo-ship)\n\n"
        markdown_content += f"**Content:**\n\n{article_text}\n\n"
        markdown_content += f"# Condensed Version (Extracted Facts)\n\n"
        for i, fact in enumerate(facts, 1):
            markdown_content += f"{i}. {fact}\n"

        # Write to a markdown file
        with open("news_summary.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print("Markdown file 'news_summary.md' has been generated.")

    else:
        print("No article to process.")


if __name__ == "__main__":
    asyncio.run(main())
