
# AI Personal Productivity (Tool-Calling) Agent 🤖

An intelligent, modular AI Agent built with **LangChain**, designed to automate daily workflows. It bridges the gap between chat interfaces and real-world actions such as managing emails, performing calculations via external APIs, and maintaining persistent task logs.

---

## 🚀 Features

- 🧠 **Intelligent Routing**  
  Uses LangChain’s `create_tool_calling_agent` to dynamically select the appropriate tool based on user intent.

- 📧 **Gmail Integration**  
  Drafts and sends emails directly via Gmail API using OAuth2 authentication.

- 📝 **Persistent Task Management**  
  Stores tasks in structured JSON format and logs them into a local `tasks.txt` file.

- 🧮 **Web-Based Calculator**  
  Performs secure, high-precision calculations using external APIs (avoids unsafe `eval()` usage).

- 📂 **Modular Tool Architecture**  
  Easily extendable system for adding tools like document search, company policies, or custom APIs.

---

## 🛠 Tech Stack

- **Language:** Python 3.13  
- **Frameworks:** LangChain, LangChain-Core  
- **UI:** Streamlit  
- **LLM Provider:** Groq Cloud (Llama 3)  
- **APIs:** Gmail API, MathJS API  

---

## 📋 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/my-ai-agent.git
cd my-ai-agent
```

---

### 2. Install Dependencies

It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, install manually:

```bash
pip install langchain langchain-openai langchain-groq langchain-community langchain-core streamlit google-api-python-client google-auth-oauthlib requests
```

---

### 3. Setup Configuration

Create a `config.py` file in the root directory:

```python
GROQ_API_KEY = "your_groq_key_here"
```

---

### 4. Gmail API Setup

1. Go to the Google Cloud Console: https://console.cloud.google.com/
2. Create a project and enable **Gmail API**
3. Download `credentials.json`
4. Place it in the root directory of the project

---

## ⚙️ How to Run

Start the Streamlit application:

```bash
python -m streamlit run src/main.py
```

---

## 🏗 Project Structure

```text
my-ai-agent/
├── src/
│   ├── main.py              # Streamlit entry point
│   ├── services/
│   │   ├── agent.py         # Core agent logic
│   │   └── tools.py         # Custom tool definitions
│   └── config.py            # API keys and config
├── credentials.json         # Google OAuth credentials
├── tasks.txt                # Persistent task storage
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 💡 How It Works (Architecture)

This agent follows a **Tool-Calling Architecture**:

1. User sends a prompt via Streamlit UI.
2. The LLM (Llama 3 via Groq) analyzes the request.
3. The agent decides whether a tool is needed (Email, Calculator, Task Manager, etc.).
4. The selected tool is executed via `AgentExecutor`.
5. The response is returned to the user with results.

This modular design allows easy extension and safe execution of external actions.

---

## 🔒 Security Notes

- No unsafe `eval()` usage for calculations
- OAuth2 used for secure Gmail authentication
- API keys stored in separate config file (not hardcoded in logic)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository  
2. Create a new branch  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes  
4. Open a Pull Request  

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Acknowledgements

- LangChain Community
- Groq Cloud
- Open-source AI ecosystem
