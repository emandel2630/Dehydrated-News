# News Fact Extraction Project

## Project Overview

The goal of this project is to strip away the narrative and bias from news articles and present pure factual statements. By doing so, we aim to compare the facts across different news sources and ensure consistency and truthfulness, ultimately reducing the risk of conflicting information.

## Example IN/OUT

### Original Article

**Title:** FBI agents board Baltimore ship linked to Singaporean company sued in bridge collapse

**URL:** [Link to article](https://www.npr.org/2024/09/21/nx-s1-5121915/fbi-baltimore-bridge-collapse-cargo-ship)

**Content:**


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


### Condensed Version (Extracted Facts)

1.  The FBI and other federal authorities boarded a vessel in Baltimore managed by the same company that managed the cargo ship that caused the collapse of the Francis Scott Key Bridge in March.
2. The Justice Department filed a lawsuit against the companies that owned and operated the ship a few days before the authorities' visit.
3. The FBI, officials from the U.S. Environmental Protection Agency’s Criminal Investigation Division, and the Coast Guard's Investigative Services arrived at the Maersk Saltoro vessel on a Saturday morning.
4. Records from IHS Shipping Data show the Maersk Saltoro is managed by Synergy Marine Private Ltd., the same company that operated the cargo ship, Dali.
5. On March 26, the Dali lost power and crashed into the Baltimore bridge, resulting in the deaths of six construction workers who had been repairing potholes on the structure overnight.
6. The Justice Department is suing Synergy Marine and the ship's owner, Grace Ocean Private Ltd., both Singapore-based corporations, for negligence and dangerous cost-cutting decisions that led to the bridge collapse.
7. The bridge collapse shut down the busy port for months and obliterated a segment of Interstate 695 carried by the bridge.
8. The federal government is seeking more than $100 million in costs that the U.S. incurred in responding to the disaster.
9. The federal claim does not cover the expenses of rebuilding the bridge and Maryland, as the builder and owner of the bridge, will pursue its own compensation according to the Justice Department.
10. The FBI has opened a criminal investigation into the fatal collapse, focusing on the massive ship and whether the crew knew that the vessel was malfunctioning before they left the port.


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


