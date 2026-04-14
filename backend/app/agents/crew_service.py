import os
import chromadb
from chromadb.utils import embedding_functions
from crewai.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from crewai import LLM, Agent, Task, Crew, Process

from app.core.config import settings
from app.models.schemas import RunResult

# Ensure API keys are available as environment variables for CrewAI/LiteLLM
if settings.NVIDIA_API_KEY:
    os.environ["NVIDIA_API_KEY"] = settings.NVIDIA_API_KEY
    # NVIDIA NIM is OpenAI-compatible — expose key as OPENAI_API_KEY for the openai provider
    os.environ["OPENAI_API_KEY"] = settings.NVIDIA_API_KEY
if settings.TAVILY_API_KEY:
    os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY


def _build_crew():
    """Build and return the 4-agent sales crew. Called once at import time."""

    persist_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "data", "chroma_db"
    )
    chroma_client = chromadb.PersistentClient(path=os.path.abspath(persist_dir))
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    personality_col = chroma_client.get_or_create_collection(
        name="personality-corpus", embedding_function=ef
    )
    product_col = chroma_client.get_or_create_collection(
        name="product-corpus", embedding_function=ef
    )

    tavily_search = TavilySearchResults(
        max_results=3, tavily_api_key=settings.TAVILY_API_KEY
    )

    @tool("tavily_search")
    def tavily_tool(query: str) -> str:
        """Searches the internet for information about people and companies."""
        return str(tavily_search.invoke({"query": query}))

    @tool("query_personality_corpus")
    def query_personality_corpus(query: str) -> str:
        """Queries the personality psychology corpus for Big Five, DISC, and buying psychology insights."""
        results = personality_col.query(query_texts=[query], n_results=3)
        docs = results.get("documents", [[]])
        return " ".join(docs[0]) if docs and docs[0] else "No relevant data."

    @tool("query_product_corpus")
    def query_product_corpus(query: str) -> str:
        """Queries the product corpus for features, benefits, and value propositions."""
        results = product_col.query(query_texts=[query], n_results=3)
        docs = results.get("documents", [[]])
        return " ".join(docs[0]) if docs and docs[0] else "No relevant data."

    llm = LLM(
        model="nvidia_nim/meta/llama-3.1-70b-instruct",
        api_key=settings.NVIDIA_API_KEY,
        base_url="https://integrate.api.nvidia.com/v1",
        temperature=0.3,
    )

    researcher = Agent(
        role="Lead Prospect Researcher",
        goal="Gather comprehensive public information about {prospect_name} at {company_name}.",
        backstory=(
            "Expert open-source intelligence analyst building detailed B2B prospect dossiers "
            "from LinkedIn, news, and company announcements."
        ),
        verbose=True,
        tools=[tavily_tool],
        llm=llm,
    )

    profiler = Agent(
        role="Psychological Profiler",
        goal=(
            "Analyze research data to score {prospect_name}'s Big Five (OCEAN) dimensions 1-10 "
            "and determine their DISC type."
        ),
        backstory=(
            "Behavioral scientist who translates professional behavior patterns into buying "
            "psychology profiles."
        ),
        verbose=True,
        tools=[query_personality_corpus],
        llm=llm,
    )

    strategist = Agent(
        role="Sales Strategist",
        goal=(
            "Map product benefits to {prospect_name}'s psychology. Rank the top 3 value "
            "propositions by psychological fit."
        ),
        backstory=(
            "Senior B2B sales strategist who connects a prospect's emotional and rational "
            "needs to the right product capabilities."
        ),
        verbose=True,
        tools=[query_product_corpus, query_personality_corpus],
        llm=llm,
    )

    copywriter = Agent(
        role="Personalized Outreach Copywriter",
        goal="Draft a 3-email sequence for {prospect_name} aligned to their psychology and the strategy brief.",
        backstory=(
            "Elite B2B copywriter who tailors tone, structure, and hooks to each prospect's "
            "decision-making style."
        ),
        verbose=True,
        tools=[query_product_corpus],
        llm=llm,
    )

    research_task = Task(
        description=(
            "Research '{prospect_name}' at '{company_name}' via Tavily Search. "
            "Find professional background, company news, role responsibilities, and pain points."
        ),
        expected_output=(
            "Structured report: Professional Background, Company Context, Recent Activity, "
            "Likely Pain Points, and Professional Goals. Minimum 300 words."
        ),
        agent=researcher,
    )

    profiling_task = Task(
        description=(
            "Using the research report, score '{prospect_name}'s Big Five dimensions (O/C/E/A/N) "
            "1-10 and identify their DISC type. Cite behavioral evidence for each score."
        ),
        expected_output=(
            "Psychological profile: Big Five scores, DISC type, buying motivators, "
            "communication style, objection patterns."
        ),
        agent=profiler,
        context=[research_task],
    )

    strategy_task = Task(
        description=(
            "Using the psychological profile, query the product corpus and identify the top 3 "
            "value propositions for '{prospect_name}' at '{company_name}'. "
            "Explain WHY each resonates psychologically."
        ),
        expected_output=(
            "Strategy brief: Top 3 value propositions with emotional hook and rational "
            "justification for each."
        ),
        agent=strategist,
        context=[profiling_task],
    )

    copywriting_task = Task(
        description=(
            "Draft a 3-email cold outreach sequence for '{prospect_name}' at '{company_name}'. "
            "Email 1: Pattern interrupt opener. "
            "Email 2: Value + social proof. "
            "Email 3: Low-friction CTA. "
            "Each email: subject line, 100-150 word body, P.S. line."
        ),
        expected_output=(
            "Three complete emails labeled Email 1, Email 2, Email 3. "
            "Each includes Subject Line, Body, and P.S. line."
        ),
        agent=copywriter,
        context=[profiling_task, strategy_task],
    )

    return Crew(
        agents=[researcher, profiler, strategist, copywriter],
        tasks=[research_task, profiling_task, strategy_task, copywriting_task],
        verbose=True,
        process=Process.sequential,
        max_rpm=4,
    )


def run_pipeline(prospect_name: str, company_name: str) -> RunResult:
    """Execute the full 4-agent pipeline and return a structured RunResult.

    Note: Crew is rebuilt per run to ensure agent goals with {prospect_name}
    and {company_name} template variables are properly interpolated for each run.
    The LLM calls are the bottleneck, not crew initialization.
    """
    crew = _build_crew()
    crew_output = crew.kickoff(
        inputs={"prospect_name": prospect_name, "company_name": company_name}
    )

    raw = str(crew_output)

    # Extract task outputs by index
    tasks_output = getattr(crew_output, "tasks_output", [])
    research_summary = tasks_output[0].raw if len(tasks_output) > 0 else ""
    profile_raw      = tasks_output[1].raw if len(tasks_output) > 1 else ""
    strategy_brief   = tasks_output[2].raw if len(tasks_output) > 2 else ""
    emails_raw       = tasks_output[3].raw if len(tasks_output) > 3 else ""

    return RunResult(
        prospect_name=prospect_name,
        company_name=company_name,
        research_summary=research_summary,
        profile_raw=profile_raw,
        personality_profile=None,
        strategy_brief=strategy_brief,
        emails_raw=emails_raw,
        email_sequence=None,
        raw_crew_output=raw,
    )
