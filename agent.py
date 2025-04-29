import os
from typing import Type
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool

# Load environment variables
load_dotenv()

def get_llm_client():
    """Connect to local vLLM API server."""
    return LLM(
        model="Qwen/Qwen2.5-1.5B-Instruct",  # Your vLLM model
        base_url="http://localhost:8000/v1", # Your vLLM server
        api_key=None  # No API key needed for local server
    )

# Simple Dummy Tool for now (replace later with PDF/File reader or Web Search)
class DummySearchTool(BaseTool):
    name: str = "Dummy Search"
    description: str = "Returns dummy search results"
    args_schema: Type[BaseModel] = BaseModel

    def _run(self, **kwargs) -> str:
        return "This is a dummy search result. (Later we can connect to real search or file loader.)"

def create_nexus_crew(query: str):
    """Set up the agents and crew"""
    search_tool = DummySearchTool()
    llm = get_llm_client()

    web_searcher = Agent(
        role="Web Searcher",
        goal="Find information related to the topic",
        backstory="An AI designed to gather knowledge.",
        verbose=True,
        allow_delegation=True,
        tools=[search_tool],
        llm=llm,
    )

    research_analyst = Agent(
        role="Research Analyst",
        goal="Analyze the collected information deeply.",
        backstory="An AI skilled at critical thinking.",
        verbose=True,
        allow_delegation=True,
        llm=llm,
    )

    technical_writer = Agent(
        role="Technical Writer",
        goal="Summarize insights into well-organized markdown.",
        backstory="An AI excellent at clear communication.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    search_task = Task(
        description=f"Search for relevant information about: {query}",
        agent=web_searcher,
        expected_output="List of raw search points.",
        tools=[search_tool]
    )

    analysis_task = Task(
        description="Analyze the raw search results into structured insights.",
        agent=research_analyst,
        expected_output="A deep structured analysis.",
        context=[search_task]
    )

    writing_task = Task(
        description="Create a clean, clear markdown document based on the analysis.",
        agent=technical_writer,
        expected_output="Final summarized markdown document.",
        context=[analysis_task]
    )

    crew = Crew(
        agents=[web_searcher, research_analyst, technical_writer],
        tasks=[search_task, analysis_task, writing_task],
        verbose=True,
        process=Process.sequential
    )

    return crew

def run_nexus(query: str):
    """Run the multi-agent research."""
    try:
        crew = create_nexus_crew(query)
        result = crew.kickoff()
        return result.raw
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    query = input("Enter your research topic: ")
    output = run_nexus(query)
    print("\n=== Research Output ===\n")
    print(output)
