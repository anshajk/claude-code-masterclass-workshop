from google.adk import Agent

from .tools import build_agenda, find_module


root_agent = Agent(
    name="workshop_guide",
    model="gemini-2.5-flash",
    description="Helps developers explore an agent-engineering workshop.",
    instruction=(
        "Help developers choose workshop modules and build a suitable agenda. "
        "Use find_module for questions about a specific topic and build_agenda "
        "for scheduling requests. Return tool errors explicitly. Do not invent "
        "modules or reveal configuration and credentials."
    ),
    tools=[find_module, build_agenda],
)
