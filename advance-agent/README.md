# Advance Agent

An Advance Agent + Chatbot built with UV, OpenAI Agents SDK, and Chainlit.

## Key Features

- **Chainlit for UI**: Modern, responsive chat interface
- **Authentication with GitHub or Google**: Secure user authentication
- **Stateful Conversations**: Persistent chat history across sessions
- **Agent with OpenAI Agents SDK**: Advanced reasoning capabilities
- **Gemini Model Integration**: Powerful language model support

## Getting Started

### 1️⃣ Install UV

First, install **UV** (if not already installed):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Windows:

```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:

```sh
uv --version
```

---

### 2️⃣ Create and Initialize the Project

```sh
uv init advance-agent
cd advance-agent
```

---

### 3️⃣ Install Dependencies

```sh
uv add chainlit python-dotenv openai-agents
```

---

### 4️⃣ Activate UV Virtual Environment (Windows)

```sh
.venv\Scripts\activate
```

For Linux/macOS:

```sh
source .venv/bin/activate
```

### 5️⃣ Try Chainlit Hello

Run the following command to check if Chainlit is installed and working:

```sh
chainlit hello
```

Go to the following URL:

```sh
http://localhost:8000
```

Enter your name and send the message

You should see the following output:

```sh
Your name is: Afaq Ul Islam / Your Name
Chainlit installation is working!
You can now start building your own chainlit apps!
```

---

### 6️⃣ Create .env file

Create a `.env` file in the root directory of the project and add the following:

```sh
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter_llm_model

OAUTH_GITHUB_CLIENT_ID=your_github_client_id
OAUTH_GITHUB_CLIENT_SECRET=your_github_client_secret

OAUTH_GOOGLE_CLIENT_ID=your_google_client_id
OAUTH_GOOGLE_CLIENT_SECRET=your_google_client_secret

CHAINLIT_AUTH_SECRET=your_chainlit_auth_secret
```

- Get OpenRouter API key from [here](https://openrouter.ai/settings/keys)

- Get OpenRouter LLM Model from [here](https://openrouter.ai/models?q=free)

- Get GitHub OAuth Client ID and Client Secret from [here](https://github.com/settings/applications)

- Get Google OAuth Client ID and Client Secret from [here](https://console.cloud.google.com/apis/credentials)

- Get chainlit auth secret with the following command:

```sh
chainlit create-secret
```

Copy the generated values and paste it in the `.env` file.

---

### 7️⃣ Create `chainlit.yaml` file

Create a `chainlit.yaml` file in the root directory of the project and add the [following code](https://github.com/afaqulislam).

---

### 8️⃣ Run Advance Agent (Web App)

```sh
chainlit run main.py -w
```

Go to the following URL:

```sh
http://localhost:8000
```

**_First login with GitHub or Google, and then enter your question and send the message, and you should see the answer from the Agent, and the Agent will remember your previous messages._**

🎉 That’s it! Your Advance Agent is ready to use 🚀
