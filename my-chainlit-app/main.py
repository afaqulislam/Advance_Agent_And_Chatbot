import os
import chainlit as cl
from dotenv import load_dotenv
from typing import Optional, Dict
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.tool import function_tool
from data import data  # ✅ Import your local portfolio data (Python dict)
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Runner

# Load environment variables
load_dotenv()

# Force HTTPS and trusted proxy headers in production
os.environ["CHAINLIT_BASE_URL"] = "https://afaqulislam-chainlit.up.railway.app"
os.environ["CHAINLIT_TRUSTED_HOSTS"] = "*"
os.environ["CHAINLIT_FORCE_HTTPS"] = "true"

# Get OpenRouter API config
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base_url = os.getenv("OPENROUTER_BASE_URL")
openrouter_model = os.getenv("OPENROUTER_MODEL")

# Initialize OpenAI provider with OpenRouter
provider = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url=openrouter_base_url,
)

# Model configuration
model = OpenAIChatCompletionsModel(model=openrouter_model, openai_client=provider)


# ✅ Function tool to fetch data locally from data.py
@function_tool("get_afaqulislam_data")
def get_afaqulislam_data() -> str:
    """
    Fetches profile data about Afaq Ul Islam from the local data.py file.

    Returns:
        str: JSON string containing Afaq Ul Islam profile information
    """
    try:
        import json

        return json.dumps(data, indent=4)
    except Exception as e:
        return f"Error loading Afaq Ul Islam data: {str(e)}"


# ✅ Agent Definition
agent = Agent(
    name="Afaq Info Agent",
    instructions="""
You are an Intelligent Agent created to represent and respond on behalf of **Afaq Ul Islam**, a professional Full Stack Developer.

Your core purpose is to interact with users, share relevant details about Afaq Ul Islam, and maintain a polished and respectful tone throughout all interactions.

---

### 🎯 DUTIES & BEHAVIOR

1. **Greetings**
   - When a user greets you (e.g., says "Hi", "Hello", "Salam", "Hey"), respond warmly with:
     → "Salam from Afaq Ul Islam 👋"
   - Always use a friendly and polite tone.

2. **Farewell**
   - When a user says goodbye, farewell, or similar (e.g., "Bye", "Khuda Hafiz", "See you"), respond with:
     → "Allah Hafiz from Afaq Ul Islam 🤍"

3. **Information Requests (Afaq Ul Islam Related)**
   - If the user asks *any question or detail related to Afaq Ul Islam* — such as:
     - Skills
     - Services
     - Projects
     - Experience
     - Education
     - Social Links
     - Contact Details
   - Then **call the tool named `get_afaqulislam_data`** to fetch and display the relevant JSON data.

   Example behavior:
   - If the user asks “What are Afaq’s skills?” → Call `get_afaqulislam_data("skills")`
   - If they ask “Show me his projects” → Call `get_afaqulislam_data("projects")`
   - If they ask for all info → Call `get_afaqulislam_data("all")`

   Make sure your responses are formatted neatly, clearly, and easy to read.

4. **General Questions**
   - If the user asks *any general or unrelated question* (e.g., about technology, education, logic, or daily topics),
     respond intelligently using your reasoning and language model capabilities.
   - Always provide accurate, concise, and easy-to-understand answers.
   - Do **not** call any tools for general questions.

5. **Tone & Style**
   - Maintain a **professional, respectful, and friendly** tone.
   - Use **clear formatting**, bullet points, and emojis when appropriate.
   - Keep answers **concise, factual, and visually structured**.

---

### ⚙️ TOOL ACCESS

You have access to **one tool**:
- **Tool Name:** `get_afaqulislam_data`
- **Purpose:** Retrieve structured data (JSON) about Afaq Ul Islam such as projects, skills, experience, and more.
- **Usage:**
  ```python
  get_afaqulislam_data("category")
""",
    model=model,
    tools=[get_afaqulislam_data],
)


# ✅ OAuth Callback (if you’re using GitHub login)
@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:

    # use these print statements for debugging
    # print(f"Provider: {provider_id}")
    # print(f"User data: {raw_user_data}")
    return default_user


# ✅ On Chat Start
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    # await cl.Message(
    #     content="👋 Salam! I'm Afaq Ul Islam's personal AI assistant. You can ask me about his skills, projects, services, and experience."
    # ).send()


# ✅ On Message
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": message.content})

    # Create an empty message placeholder on frontend
    msg = cl.Message(content="")
    await msg.send()

    # Start streaming response from the agent
    result = Runner.run_streamed(agent, input=history)

    full_response = ""  # to store final response

    async for event in result.stream_events():
        # Only handle text delta events (partial text updates)
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            delta = event.data.delta
            full_response += delta
            await msg.stream_token(delta)  # send partial text to frontend live

    # Update final message content after streaming completes
    await msg.update()

    # Save final response to chat history
    history.append({"role": "assistant", "content": full_response})
    cl.user_session.set("history", history)
