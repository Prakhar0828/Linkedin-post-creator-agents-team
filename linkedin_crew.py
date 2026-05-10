# Imports
from pathlib import Path

from crewai import Agent, Task, Crew, Process, tools
from crewai_tools import SerperDevTool, YoutubeVideoSearchTool, DirectorySearchTool, DallETool


# Parent directory that contains one subfolder per skill (each with SKILL.md).
_SKILLS_ROOT = Path(__file__).resolve().parent / "skills"

# Define tools
youtube_research_tool = YoutubeVideoSearchTool()
web_research_tool = SerperDevTool()
dalle_tool = DallETool(
    model="dall-e-3",
    size="1024x1024",
    quality="standard",
    n=1
)

# Define Agents
youtube_researcher_agent = Agent(
    role = "Youtube Researcher",
    goal = "Extract the most valuable insights from a YouTube video about {topic}",
    backstory = """You are an expert at analyzing video content and extracting the key takeaways
    that audiences find most valuable. You focus on unique perspectives, memorable
    quotes, frameworks, and actionable advice shared in the video. You always note
    the speaker's main argument and supporting points."""
)

web_researcher_agent = Agent(
    role = "Web Researcher",
    goal = "Find the latest and most insightful information about {topic} from the web",
    backstory = """You are a senior research analyst who excels at finding high-quality, recent
    information from the internet. You focus on finding unique insights, statistics,
    expert opinions, and real-world examples that would make great talking points for
    a LinkedIn post. You ignore fluff and focus on substance.""",
    verbose = True
)

linkedin_writer_agent = Agent(
    role = "Linkedin Post Writer",
    goal = "Write a viral LinkedIn post about {topic} that gets high engagement",
    backstory = """You are a top LinkedIn ghostwriter who has written posts for tech leaders with
    millions of impressions. You know that great LinkedIn posts start with a killer
    hook in the first line, use short punchy paragraphs, tell a story or share a
    strong opinion, and end with a clear takeaway or question. You never write
    generic corporate fluff — every post has personality and edge.""",
    verbose = True,
    skills=["/Users/prakhar/Documents/Knowledge Base/Linked-Writer-Agent/skills"],
)

image_creator = Agent(
    role="LinkedIn Post Image Creator",
    goal="Create a visually striking image that complements the LinkedIn post about {topic}",
    backstory=(
        "You are a creative director who specializes in creating "
        "scroll-stopping visuals for social media. You know that "
        "LinkedIn images should be professional yet eye-catching, "
        "and should visually represent the core idea of the post. "
        "You create clean, modern images that make people stop "
        "scrolling and read the post."
    ),
    tools=[dalle_tool],
    verbose=True,
    allow_delegation=False
)
# Define Tasks
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
    agent = youtube_researcher_agent
)

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
    output_file = "linkedin_post.md",
    context = [web_research_task]
)

task_create_image = Task(
    description=(
        "Based on the LinkedIn post that was written, create an image "
        "that would be the perfect visual accompaniment.\n\n"
        "The image should:\n"
        "- Visually represent the core theme of the post\n"
        "- Be professional and suitable for LinkedIn\n"
        "- Be eye-catching enough to stop someone from scrolling\n"
        "- NOT contain any text or words in the image\n"
        "- Use a clean, modern aesthetic\n\n"
        "Generate a detailed prompt for DALL-E and create the image."
    ),
    expected_output=(
        "The URL or file path of the generated image, along with "
        "the DALL-E prompt that was used to create it."
    ),
    agent=image_creator,
    context=[linkedin_writing_task]
)
# Define the team/crew
crew = Crew(
    agents = [web_researcher_agent, youtube_researcher_agent, linkedin_writer_agent, image_creator],
    tasks = [web_research_task, linkedin_writing_task, task_create_image],
    process = Process.sequential,
    verbose=True,
)

# Run the crew
result = crew.kickoff(inputs={"topic": "AI", "youtube_video_url": "https://www.youtube.com/watch?v=baoTpwmIBbU"})
print(result.raw)