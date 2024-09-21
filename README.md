# News Fact Extraction Project

## Project Overview

The goal of this project is to strip away the narrative and bias from news articles and present pure factual statements. By doing so, we aim to compare the facts across different news sources and ensure consistency and truthfulness, ultimately reducing the risk of conflicting information.

## Code Structure

### 1. `NewsFetcher` Class
- **Purpose:** This class is responsible for fetching news articles from the NewsAPI. It allows for retrieving articles published on the current date, either with or without a specific query.
- **Methods:**
  - `fetch_news_articles`: Fetches a single page of articles. Accepts an optional query parameter to filter articles based on specific keywords.
  - `fetch_all_articles`: Fetches multiple pages of articles asynchronously and accumulates them into a single list.

### 2. `WorldNewsFetcher` Class
- **Purpose:** This class fetches top news articles from the World News API, focusing on US-based sources.
- **Methods:**
  - `fetch_top_news`: Retrieves the top news articles for the current date. It uses the World News API, which requires a different API key and request structure compared to NewsAPI.

### 3. `FactExtractor` Class
- **Purpose:** This class is designed to extract pure factual statements from the content of news articles using OpenAI's language model.
- **Methods:**
  - `extract_facts`: Given the text of a news article, this method uses a prompt-based approach to extract and present factual statements as a numbered list. It caches results to avoid redundant API calls.

### 4. `main()` Function
- **Purpose:** The `main` function orchestrates the entire process of fetching news articles, extracting facts, and writing the results to a text file.
- **Steps:**
  1. **Initialize Fetchers:** Instances of `NewsFetcher`, `WorldNewsFetcher`, and `FactExtractor` are created.
  2. **Fetch Articles:** The function fetches news articles (e.g., related to a specific query like "apple") and optionally fetches top news from other sources.
  3. **Process and Extract Facts:** For each article, the factual content is extracted and written to a report file, alongside the article's title and URL.
  4. **Output:** A text report (`news_report.txt`) is generated, containing all extracted facts organized by source.

## Future Plans

As the project evolves, the focus will shift towards comparing factual statements across different news sources. The goal is to identify and highlight any conflicting information. Enhancements planned include:

- **Fact Comparison:** Develop logic to compare facts extracted from different sources and highlight any discrepancies.
- **Source Analysis:** Implement algorithms to assess the reliability of different sources based on the consistency of facts they provide.
- **Expanded Coverage:** Extend the project to include more news sources and APIs to ensure a broad and diverse range of information.

## Dependencies

- **Python 3.8+**
- **aiohttp**: For making asynchronous HTTP requests.
- **httpx**: For HTTP/2 requests, offering better performance.
- **openai**: For interfacing with OpenAI's API.
- **langchain**: To help with prompt-based fact extraction using OpenAI.
- **dotenv**: For managing API keys and environment variables.


