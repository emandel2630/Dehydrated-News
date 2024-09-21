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

print(NEWS_API_KEY)

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
                openai_api_key=openai.api_key, model_name="gpt-4o", temperature=0.5
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
    article = await news_fetcher.fetch_news_article(query)

    if article:
        # article_title = article.get("title", "No Title")
        # article_url = article.get("url", "No URL")
        # article_text = article.get("content") or article.get("description") or ""

        # # Print the original article
        print("Original Article:")
        # print(f"Title: {article_title}")
        # print(f"URL: {article_url}")
        # print(f"Content:\n{article_text}\n")

        article_text = """
 In Kamala Harris, the Democrats have created the
biggest soap bubble American politics has ever seen. The question
is, can they stop Donald Trump popping it until Nov. 5? Photo: Erin
Hooley/Associated Press
The race is deadlocked with six weeks to go and
if you’re an undecided, unsure or wavering voter
it looks like Awful vs. Empty.
Kamala Harris has made quite an impression.
That walk is a stride, and she has appetite—she
loves this thing, running for high office. She has
sentiments—she loves to say what divides us
isn’t as big as what unites us, which, though a
dreadful cliché, is true.
Advertisement
But in terms of policy she is coming across as
wholly without substance.
Joe Biden stepped aside, and Ms. Harris was
elevated, two months ago. That is enough time
at least to start making clear what she believes,
wants and means to do. She hasn’t.
This week she couldn’t or wouldn’t answer a
single question straight, and people could see it.
She is an artless dodger.
In her unscripted 11-minute interview with
ABC’s Philadelphia station on Tuesday, the
reporter asked, meekly, for “one or two specific
things you have in mind” to get prices down.
Advertisement
Ms. Harris: “Well, I’ll start with this: I grew up a
middle-class kid. My mother raised my sister
and me. She worked very hard. She was able to
finally save up enough money to buy our first
house when I was a teenager. I grew up in a
community of hardworking people, you know,
construction workers and nurses and teachers.
And I try to explain to some people who may not
have had the same experience, you know, if—but
a lot of people will relate to this. You know, I
grew up in a neighborhood of folks who were
very proud of their lawn, you know? And I was
raised to believe and to know that all people
deserve dignity, and that we as Americans have
a beautiful character, you know, we have
ambitions and aspirations and dreams. But not
everyone necessarily has access to the resources
that can help them fuel those dreams and
ambitions. So when I talk about building an
opportunity economy, it is very much with the
mind of investing in the ambitions and
aspirations and the incredible work ethic of the
American people . . .” On it went, with a few
policy ideas tacked on at the end.
Also from the interview: “Focusing on, again,
the aspirations and the dreams but also just
recognizing that at this moment in time, some of
the stuff we could take for granted years ago, we
can’t take for granted anymore.” “And so my
approach is about new ideas, new policies that
are directed at the current moment, and also to
be very honest with you, my focus is very much
on what we need to do over the next ten, twenty
years. To catch up to the 21st century around,
again, capacity but also challenges.”
This is word-saying gibberish. Only when
speaking of her personal biography does she
seem authoritative. Otherwise she is airy,
evasive, nonresponsive.
Advertisement
How to appeal to Trump voters who might be
open to her? “I, based on experience, and a lived
experience, know in my heart, I know in my soul,
I know that the vast majority of us as Americans
have so much more in common than what
separates us. And I also believe that I am
accurate in knowing that most Americans want
a leader who brings us together as
Americans . . .”
That isn’t the answer of a candidate trying to be
forthcoming and using her limited time in an
attempt to be better understood. It is the sound
of someone running out the clock.
In an appearance Tuesday at the National
Association of Black Journalists, Ms. Harris was
asked about increasing her support among black
men.
“The policies and the perspectives I have
understands what we must do to recognize the
needs of all communities, and I intend to be a
president for all people . . .” Again, she spoke of
her “economic opportunity tour.”
Advertisement
Why does she dodge away from clarity? Why
doesn’t she take opportunities to deepen public
understanding of her thinking?
Here are some guesses, one or more of which
may be correct.
• Because she’s not that interested in policy. This
would be strange, because politics is the policy
business; that’s what politicians make. But she
forged her political life in California, where
politics is an offshoot of its other great industry,
show business. It is possible that she views
policy as just something you have to do to
advance your personal standing and enjoy being
on top. It is clear she has memorized certain
position points (help small businesses) that
have perhaps been urged on her by professionals
who do politics for a living.
• Because she’ll figure it out later. Specificity
divides while sentiment gathers.
Advertisement
• Because she doesn’t want you to understand
where she stands. Because she’s more
progressive than she admits, and there’s no gain
in telling you now.
• Because at bottom she’s as progressive as Joe
Biden, meaning as progressive as the traffic will
bear. But that would mean she’s more of the
same, so why talk about it?
READ MORE DECLARATIONS
A Decisive but Shallow Debate Win for
Harris September 12, 2024
Trump and Harris Get Set to Debate September 5,
2024
Some supporters think she needs to be more
“specific,” but it isn’t specificity per se that is
the glaring omission. Her problem is not that
she doesn’t say she’ll repeal section 13(c) of
some regulatory act. No one knows what 13(c) is.
What people want to hear, and deserve to hear,
is her essential meaning and purpose as a
political figure. It’s not about data points and
the arcana of government; it’s about belief and
the philosophical underpinnings of that belief.
What are her thoughts, right now, about illegal
immigration and the border? After the past
three years of a historic influx she said in the
debate that she’d hire more border agents. Why?
Toward what end, in pursuit of what larger
goal?
Advertisement
Was the influx a good thing? Why? Does it
constitute a national emergency? Why? What
attitude does she bring to this crucial question?
Failing to speak plainly and deeply now about
illegal immigration is political malpractice on a
grand scale. There are other large questions.
What philosophical predilection does she bring
to taxing, spending, regulation, to the national
debt?
She owes us these answers. It is wrong that she
can’t or won’t address them. It is disrespectful
to the electorate.
If voters don’t get a sense of her deeper beliefs
they will think of her as a construct, something
other people built so they can run the country as
she does photo-ops. Half of America wonders
who’s really running things as the Biden years
ebb. They won’t want to wonder for another four
years.
Which gets us back to Awful vs. Empty. When
Americans feel that’s the choice and neither side
gives them reason to believe otherwise, they’ll
likely start to think in ways they believe
practical. Empty means trouble, a blur when we
need a rudder, a national gamble based on
insufficient information. It means a policy
regime that would be unpredictable, perhaps
extreme. You don’t want that.
Awful is—well, awful. But he was president for
four years, we didn’t all explode, institutions
held, the threatened Constitution maintained.
So—maybe that’s their vote. “Close your eyes
and think of England.”
Unless of course in the next six weeks somebody
surprises them, and impresses them.
Kamala Harris speaks at a discussion hosted by the National
Association of Black Journalists in Philadelphia, Sept. 17.
PHOTO: JIM WATSON/AGENCE FRANCE-PRESSE/GETTY IMAGES
Advertisement
•
•
“Declarations” seeks the truth and then tries to state
that truth. The column is published online every
Thursday evening and aims to give clarity and humor
where appropriate. It is isn’t overtly ideological and
asks the reader to be open to diferent considerations.
Peggy Noonan is an opinion columnist at the Wall
Street Journal where her column, "Declarations," has
run since 2000.
She was awarded the Pulitzer Prize for Commentary
in 2017. A political analyst for NBC News, she is the


"""
        print(article_text)

        # Extract facts
        facts = await fact_extractor.extract_facts(article_text)

        # Print the condensed version
        print("Condensed Version (Extracted Facts):")
        for fact in facts:
            print(f"- {fact}")

    else:
        print("No article to process.")


if __name__ == "__main__":
    asyncio.run(main())
