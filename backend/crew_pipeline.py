import os
import sys
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("ANTHROPIC_API_KEY") or not os.environ.get("TAVILY_API_KEY"):
    print("Error: ANTHROPIC_API_KEY and TAVILY_API_KEY are required.")
    sys.exit(1)

import chromadb
from chromadb.utils import embedding_functions
from crewai.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from crewai import LLM, Agent, Task, Crew, Process

# 1. Initialize ChromaDB
persist_directory = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
client = chromadb.PersistentClient(path=persist_directory)
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

personality_collection = client.get_or_create_collection(
    name="personality-corpus", embedding_function=sentence_transformer_ef
)
product_collection = client.get_or_create_collection(
    name="product-corpus", embedding_function=sentence_transformer_ef
)

# 2. Setup Tools
tavily_client = TavilySearchResults(max_results=3)


@tool("tavily_search")
def tavily_tool(query: str) -> str:
    """Searches the internet for comprehensive information about people and companies."""
    return str(tavily_client.invoke({"query": query}))


@tool("query_personality_corpus")
def query_personality_corpus(query: str) -> str:
    """Queries the ChromaDB personality psychology corpus for insights on Big Five traits, DISC profiles, and buying psychology."""
    results = personality_collection.query(query_texts=[query], n_results=3)
    return " ".join(results["documents"][0]) if results["documents"] else "No relevant data."


@tool("query_product_corpus")
def query_product_corpus(query: str) -> str:
    """Queries the ChromaDB product corpus for features, benefits, and value propositions."""
    results = product_collection.query(query_texts=[query], n_results=3)
    return " ".join(results["documents"][0]) if results["documents"] else "No relevant data."


# 3. Initialize LLM (Anthropic Claude)
llm = LLM(
    model="anthropic/claude-opus-4-6",
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    temperature=0.3,
)

# 4. Define Agents

researcher = Agent(
    role="Lead Prospect Researcher",
    goal="Gather comprehensive public information about {prospect_name} at {company_name}, including their professional background, recent activity, and company context.",
    backstory=(
        "You are an expert open-source intelligence analyst who specializes in building "
        "detailed dossiers on B2B prospects. You find professional insights from LinkedIn, "
        "news articles, and company announcements."
    ),
    verbose=True,
    tools=[tavily_tool],
    llm=llm,
)

profiler = Agent(
    role="Psychological Profiler",
    goal=(
        "Analyze the research data to deduce {prospect_name}'s probable personality profile "
        "using Big Five (OCEAN) and DISC frameworks. Score each dimension 1-10."
    ),
    backstory=(
        "You are a buying psychology expert trained in behavioral science. You translate "
        "professional behavior patterns into actionable personality profiles that predict "
        "how someone makes purchasing decisions."
    ),
    verbose=True,
    tools=[query_personality_corpus],
    llm=llm,
)

strategist = Agent(
    role="Sales Strategist",
    goal=(
        "Map {company_name}'s product benefits directly to {prospect_name}'s psychological "
        "profile and professional pain points. Produce a ranked list of the top 3 value "
        "propositions that will resonate most with this specific prospect."
    ),
    backstory=(
        "You are a senior B2B sales strategist who bridges the gap between a prospect's "
        "psychology and a product's capabilities. You identify which features solve which "
        "emotional and rational needs for a specific buyer persona."
    ),
    verbose=True,
    tools=[query_product_corpus, query_personality_corpus],
    llm=llm,
)

copywriter = Agent(
    role="Personalized Outreach Copywriter",
    goal=(
        "Draft a precise 3-email sequence for {prospect_name} that maps directly to their "
        "psychological profile and the strategist's recommended value propositions."
    ),
    backstory=(
        "You are an elite B2B copywriter who writes hyper-personalized cold email sequences. "
        "You adapt tone, structure, and messaging to match the prospect's communication style "
        "and decision-making drivers."
    ),
    verbose=True,
    tools=[query_product_corpus],
    llm=llm,
)

# 5. Define Tasks

research_task = Task(
    description=(
        "Research '{prospect_name}' at '{company_name}' using Tavily Search. "
        "Find their LinkedIn profile details, recent posts, company news, and role responsibilities. "
        "Identify their likely KPIs, challenges, and professional motivations."
    ),
    expected_output=(
        "A structured report with sections: Professional Background, Company Context, "
        "Recent Activity, Likely Pain Points, and Professional Goals. Minimum 300 words."
    ),
    agent=researcher,
)

profiling_task = Task(
    description=(
        "Using the research report, query the personality corpus and analyze '{prospect_name}'s "
        "likely personality. Score Big Five dimensions (Openness, Conscientiousness, Extraversion, "
        "Agreeableness, Neuroticism) 1-10 and determine their DISC type (D/I/S/C). "
        "Explain the behavioral evidence behind each score."
    ),
    expected_output=(
        "A psychological profile containing: Big Five scores (O/C/E/A/N each 1-10), "
        "DISC type, primary buying motivators, communication style preferences, "
        "and key objection patterns. Format as structured JSON-like output."
    ),
    agent=profiler,
    context=[research_task],
)

strategy_task = Task(
    description=(
        "Using '{prospect_name}'s psychological profile and their role at '{company_name}', "
        "query the product corpus and identify the top 3 product value propositions "
        "that will resonate most. Explain WHY each resonates based on their psychology."
    ),
    expected_output=(
        "A strategy brief with: Top 3 value propositions ranked by psychological fit, "
        "the emotional hook for each, the rational justification for each, "
        "and recommended messaging angles. Format clearly with headers."
    ),
    agent=strategist,
    context=[profiling_task],
)

copywriting_task = Task(
    description=(
        "Draft a 3-email cold outreach sequence for '{prospect_name}' at '{company_name}'. "
        "Email 1: Pattern interrupt opener using their top psychological driver. "
        "Email 2: Value + social proof aligned to their DISC type. "
        "Email 3: Low-friction CTA matching their decision style. "
        "Each email: subject line, 100-150 words body, P.S. line."
    ),
    expected_output=(
        "Three complete emails. Each email must include: Subject Line, Body (100-150 words), "
        "and a P.S. line. Clearly labeled Email 1, Email 2, Email 3."
    ),
    agent=copywriter,
    context=[profiling_task, strategy_task],
)

# 6. Assemble Crew
sales_crew = Crew(
    agents=[researcher, profiler, strategist, copywriter],
    tasks=[research_task, profiling_task, strategy_task, copywriting_task],
    verbose=True,
    process=Process.sequential,
    max_rpm=4,
)

if __name__ == "__main__":
    print("SalesNeuro CrewAI Pipeline (Anthropic Claude)...")
    result = sales_crew.kickoff(
        inputs={
            "prospect_name": "VP of Engineering",
            "company_name": "an industrial robotics company",
        }
    )
    print("\n\n### FINAL CREW OUTPUT ###\n")
    print(result)
