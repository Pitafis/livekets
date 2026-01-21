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

# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# from livekit.agents import (
#     Agent,
#     AgentServer,
#     AgentSession,
#     JobContext,
#     RunContext,
#     cli,
#     function_tool,
# )
# from livekit.plugins import silero
# from livekit.plugins import deepgram  # <-- Add this
# from livekit.plugins import elevenlabs  # <-- Add this

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
#         stt=deepgram.STT(
#             model="nova-3",      # Or "nova-2", "flux-general" for even lower latency
#             language="en",
#         ),
#         llm="openai/gpt-4o-mini",
#         tts=elevenlabs.TTS(
#             model="eleven_turbo_v2_5",
#             voice_id="21m00Tcm4TlvDq8ikWAM",  # ← Your chosen voice ID here
#             # streaming_latency=3,  # Optional: tune latency (1=fastest, higher=more stable)
#         ),
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
# Note: For ElevenLabs STT/TTS via plugins or inference
from livekit.plugins import elevenlabs  # For TTS plugin
# Deepgram removed since it doesn't support Urdu well

@function_tool
async def lookup_weather(context: RunContext, location: str = "Karachi"):
    """موجودہ موسم کی معلومات حاصل کریں۔"""
    # Simulate real weather data (in real app, call an API here)
    return {
        "location": location,
        "weather": "صاف آسمان اور ہلکی ہوا",
        "temperature_c": 25,
        "temperature_f": 77,
        "feels_like_c": 26,
    }

server = AgentServer()

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        vad=silero.VAD.load(),
        # Use ElevenLabs Scribe for STT (supports Urdu among 90+ languages)
        stt="elevenlabs/scribe_v2_realtime",  # Via LiveKit Inference (best for multilingual incl. Urdu)
        # Optional: language="ur" if you want to force Urdu detection
        llm="openai/gpt-4o-mini",  # LLM handles Urdu well
        tts=elevenlabs.TTS(
            model="eleven_turbo_v2_5",  # Supports Urdu (low latency multilingual)
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Replace with a Urdu/Pakistani voice ID from ElevenLabs
            # streaming_latency=3,  # Optional for tuning
        ),
    )

    agent = Agent(
        instructions="""
        آپ کا نام "Grok Helper" ہے۔ آپ دانیال کے ذاتی AI وائس اسسٹنٹ ہیں۔
        آپ دوستانہ، مددگار اور قدرتی طور پر بات کرتے ہیں جیسے ایک حقیقی شخص۔
        آپ کراچی، پاکستان میں رہتے ہیں اور مقامی سیاق و سباق کو سمجھتے ہیں۔
        جوابات مختصر، گرم جوش اور دلچسپ رکھیں۔
        اگر موسم کے بارے میں پوچھا جائے تو lookup_weather ٹول استعمال کریں۔
        صارفین کا شائستہ انداز میں استقبال کریں اور انہیں خوش آمدید کہیں۔
        ہمیشہ اردو میں بات کریں۔
        """,
        tools=[lookup_weather],
    )

    await session.start(agent=agent, room=ctx.room)

    await session.generate_reply(
        instructions="صارف کا گرمجوشی سے استقبال کریں، اپنا نام Grok Helper بتائیں، اور پوچھیں کہ آج آپ کی کیا مدد کر سکتا ہوں۔"
    )

if __name__ == "__main__":
    cli.run_app(server)
