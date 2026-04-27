import asyncio
import os
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, cartesia, silero
from openai import AsyncOpenAI

# Connexion à Together AI (API compatible OpenAI)
together_client = AsyncOpenAI(
    api_key=os.environ key_CaUejawXu514padP9xA4f,
    base_url="https://api.together.xyz/v1",
)

# Wrapper pour que LiveKit puisse utiliser Hermes
class HermesLLM(llm.LLM):
    async def chat(self, chat_ctx: llm.ChatContext, **kwargs):
        messages = [
            {"role": m.role, "content": m.content}
            for m in chat_ctx.messages
        ]
        stream = await together_client.chat.completions.create(
            model="NousResearch/Hermes-3-Llama-3.1-70B-Turbo",
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            if delta:
                yield llm.ChatChunk(
                    choices=[llm.Choice(delta=llm.ChoiceDelta(content=delta))]
                )

# Fonction principale de l'agent
async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram.STT(language="fr"),
        llm=HermesLLM(),
        tts=cartesia.TTS(
            voice=os.environ faa75703-00e3-4a57-9955-0703001e3231,
            model="sonic-multilingual",
        ),
        chat_ctx=llm.ChatContext().append(
            role="system",
            text=(
                "Tu es un assistant vocal intelligent et bienveillant. "
                "Tu réponds en français, de façon concise et naturelle. "
                "Tes réponses doivent être courtes car elles seront lues à voix haute."
            ),
        ),
    )

    assistant.start(ctx.room)

    # Message de bienvenue au démarrage
    await asyncio.sleep(1)
    await assistant.say(
        "Bonjour, je suis prêt. Comment puis-je vous aider ?",
        allow_interruptions=True,
    )

    # L'agent tourne indéfiniment jusqu'à déconnexion
    await asyncio.sleep(3600)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
