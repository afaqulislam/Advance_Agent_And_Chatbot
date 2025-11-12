# main.py (same as before)
import os
import chainlit as cl
from dotenv import load_dotenv
from typing import Optional, Dict
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.tool import function_tool
from data import data
import json

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base_url = os.getenv("OPENROUTER_BASE_URL")
openrouter_model = os.getenv("OPENROUTER_MODEL")

if not all([openrouter_api_key, openrouter_base_url, openrouter_model]):
    raise ValueError("Missing OpenRouter env vars!")

provider = AsyncOpenAI(api_key=openrouter_api_key, base_url=openrouter_base_url)
model = OpenAIChatCompletionsModel(model=openrouter_model, openai_client=provider)


@function_tool("get_afaqulislam_data")
def get_afaqulislam_data(category: str = "all") -> str:
    category = category.lower().strip()
    mapping = {
        "skills": "skills",
        "projects": "projects",
        "experience": "experience",
        "education": "education",
        "social": "social_links",
        "contact": "contact",
        "services": "services_offered",
    }
    key = mapping.get(category)
    if key and key in data:
        return json.dumps({key: data[key]}, indent=2)
    elif category == "all":
        return json.dumps(data, indent=2)
    else:
        return f"Invalid category: `{category}`"


agent = Agent(
    name="Afaq Ul Islam AI Assistant",
    instructions="""
You are Afaq Ul Islam's AI assistant.
- Greet: "Salam from Afaq Ul Islam"
- Farewell: "Allah Hafiz from Afaq Ul Islam"
- Use tool for Afaq info
- NEVER show raw JSON
- Respond in clean, natural language
""",
    model=model,
    tools=[get_afaqulislam_data],
)


@cl.oauth_callback
def oauth_callback(
    provider_id: str, token: str, raw_user_data: Dict[str, str], default_user: cl.User
):
    print(f"OAuth: {provider_id} | {raw_user_data.get('login')}")
    return default_user


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])


@cl.on_message
async def on_message(message: cl.Message):
    if message.content.strip().lower() == "debug":
        await cl.Message(
            content=f"Base URL: `{cl.request.base_url}`\n"
            f"Scheme: `{cl.request.scope.get('scheme')}`"
        ).send()
        return

    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    full_response = ""
    try:
        result = Runner.run_streamed(agent, input=history)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, "delta"):
                delta = event.data.delta
                if '{"category"' in delta:
                    continue
                full_response += delta
                await msg.stream_token(delta)

        msg.content = full_response
        await msg.update()

        history.append({"role": "assistant", "content": full_response})
        cl.user_session.set("history", history)
    except Exception as e:
        msg.content = f"Error: {e}"
        await msg.update()
        print(e)
