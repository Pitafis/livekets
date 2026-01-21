# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# from livekit.agents import (
#     Agent,
#     AgentServer,
#     AgentSession,
#     JobContext,
#     RunContext,  # <-- Needed for type hint
#     cli,
#     function_tool,
# )
# from livekit.plugins import silero

# @function_tool
# async def lookup_weather(context: RunContext, location: str = "Karachi"):
#     """Get current weather for a location."""
#     # Simulate real weather data (in real app, call an API here)
#     return {
#         "location": location,
#         "weather": "clear sky with mild breeze",
#         "temperature_c": 25,
#         "temperature_f": 77,
#         "feels_like_c": 26,
#     }

# server = AgentServer()

# @server.rtc_session()
# async def entrypoint(ctx: JobContext):
#     session = AgentSession(
#         vad=silero.VAD.load(),
#         stt="assemblyai/universal-streaming",
#         llm="openai/gpt-4o-mini",
#         tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
#     )

#     agent = Agent(
#         instructions="""
#         You are Daniyal's personal AI voice assistant named "Grok Helper".
#         You are friendly, helpful, and speak naturally like a real person.
#         You live in Karachi, Pakistan, and understand local context.
#         Keep responses short, warm, and engaging.
#         If asked about weather, use the lookup_weather tool.
#         Greet users politely and make them feel welcome.
#         """,
#         tools=[lookup_weather],
#     )

#     await session.start(agent=agent, room=ctx.room)

#     await session.generate_reply(
#         instructions="Greet the user warmly, say your name is Grok Helper, and ask how you can help today."
#     )

# if __name__ == "__main__":
#     cli.run_app(server)

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    RunContext,
    cli,
    function_tool,
)
from livekit.plugins import silero
from livekit.plugins import deepgram  # <-- Add this
from livekit.plugins import elevenlabs  # <-- Add this

@function_tool
async def lookup_weather(context: RunContext, location: str = "Karachi"):
    """Get current weather for a location."""
    # Simulate real weather data (in real app, call an API here)
    return {
        "location": location,
        "weather": "clear sky with mild breeze",
        "temperature_c": 25,
        "temperature_f": 77,
        "feels_like_c": 26,
    }

server = AgentServer()

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(
            model="nova-3",      # Or "nova-2", "flux-general" for even lower latency
            language="en",
        ),
        llm="openai/gpt-4o-mini",
        tts=elevenlabs.TTS(
            model="eleven_turbo_v2_5",
            voice_id="21m00Tcm4TlvDq8ikWAM",  # ← Your chosen voice ID here
            # streaming_latency=3,  # Optional: tune latency (1=fastest, higher=more stable)
        ),
    )

    agent = Agent(
        instructions="""
        You are Daniyal's personal AI voice assistant named "Grok Helper".
        You are friendly, helpful, and speak naturally like a real person.
        You live in Karachi, Pakistan, and understand local context.
        Keep responses short, warm, and engaging.
        If asked about weather, use the lookup_weather tool.
        Greet users politely and make them feel welcome.
        """,
        tools=[lookup_weather],
    )

    await session.start(agent=agent, room=ctx.room)

    await session.generate_reply(
        instructions="Greet the user warmly, say your name is Grok Helper, and ask how you can help today."
    )

if __name__ == "__main__":
    cli.run_app(server)