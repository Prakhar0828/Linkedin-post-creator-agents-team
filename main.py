import os
from pathlib import Path

from dotenv import load_dotenv

_env_file = Path(__file__).resolve().parent / "writer_agent" / ".env"
load_dotenv(_env_file)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
MODEL = os.getenv("MODEL")

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, YoutubeVideoSearchTool

from crew import web_research_task, youtube_research_task


# Define Tools
web_research_tool = SerperDevTool()
youtube_research_tool = YoutubeVideoSearchTool()

# Define Agents
web_researcher_agent = Agent(
    role = "Web Researcher",
    goal = "Find the latest and most insightful information about {topic} from the web",
    backstory = """You are a senior research analyst who excels at finding high-quality, recent
    information from the internet. You focus on finding unique insights, statistics,
    expert opinions, and real-world examples that would make great talking points for
    a LinkedIn post. You ignore fluff and focus on substance.""",
)
youtube_research_agent = Agent(
    role = "YouTube Researcher",
    goal = "Extract the most valuable insights from a YouTube video about {topic}",
    backstory = """You are an expert at analyzing video content and extracting the key takeaways
    that audiences find most valuable. You focus on unique perspectives, memorable
    quotes, frameworks, and actionable advice shared in the video. You always note
    the speaker's main argument and supporting points."""
)

linkedin_writer_agent = Agent(
    role = "LinkedIn Writer",
    goal = "Write a viral LinkedIn post about {topic} that gets high engagement",
    backstory = """You are a top LinkedIn ghostwriter who has written posts for tech leaders with
    millions of impressions. You know that great LinkedIn posts start with a killer
    hook in the first line, use short punchy paragraphs, tell a story or share a
    strong opinion, and end with a clear takeaway or question. You never write
    generic corporate fluff — every post has personality and edge.""",
)

# Define Tasks
web_research_task = Task(
    description="""Research the topic '{topic}' on the web.

    Find:
    - 3-5 key insights or trends about this topic
    - Any interesting statistics or data points
    - Expert opinions or hot takes
    - Real-world examples or case studies

    Focus on recent, high-quality sources. This research will be used to write a LinkedIn post.""",
    expected_output = """A research brief with 3-5 key insights about {topic}, including relevant stats,
    expert opinions, and examples. Each insight should be a short paragraph.""",
    agent = web_researcher_agent
)
youtube_research_task = Task(
    description="""Analyze the YouTube video at {youtube_video_url} about the topic '{topic}'.

    Extract:
    - The speaker's main argument or thesis
    - 3 most valuable takeaways from the video
    - Any memorable quotes or frameworks mentioned
    - Practical advice or actionable tips shared

    This research will be used to write a LinkedIn post.""",
    expected_output = """A summary of the video's key insights including the main argument, top 3 takeaways,
    notable quotes, and actionable advice.""",
    agent = youtube_research_agent
)

linkedin_writing_task = Task(
    description="""Using the web research and YouTube video insights provided to you, write a LinkedIn post about '{topic}'.

    Post requirements:
    - Start with a strong hook (first line should stop the scroll)
    - Keep it between 150-300 words
    - Use short paragraphs (1-2 sentences each)
    - Include insights from BOTH the web research and the video
    - End with a question or call-to-action to drive comments
    - Add 3-5 relevant hashtags at the end
    - Tone: professional but conversational, opinionated, not generic

    Do NOT use emojis excessively. Max 2-3 emojis in the entire post.""",
    expected_output = """A ready-to-publish LinkedIn post between 150-300 words, with a strong hook,
    insights from research, and a closing CTA. Include hashtags at the end.""",
    agent = linkedin_writer_agent,
    human_input=True,
    output_file = "linkedin_post.md",
    context = [web_research_task, youtube_research_task]
)

# Define Crew

crew = Crew(
    agents = [web_researcher_agent, youtube_research_agent, linkedin_writer_agent],
    tasks=[web_research_task, youtube_research_task, linkedin_writing_task],
    process = Process.sequential,
)
# Run the Crew
result = crew.kickoff(inputs={"topic":"AI Agents", "youtube_video_url":"https://www.youtube.com/watch?v=baoTpwmIBbU"})
print(result.raw)