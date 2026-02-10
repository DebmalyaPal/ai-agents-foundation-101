# AI Agents Foundation 101

A beginner-friendly collection of AI Agents built with Python. Learning to build agents from scratch using LLMs and tools, all in a single monorepo structure.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- An API key from [Groq](https://console.groq.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/debmalyapal/ai-agents-foundation-101.git
   cd ai-agents-foundation-101
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Mac/Linux (for Windows: venv\Scripts\activate)
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
   **(See `.env-sample` for a reference template)**

---

## 📂 Project Structure

```
ai-agents-foundation-101/
├── common/                # 🧠 Shared Brain & Tools
│   ├── __init__.py        # Makes folder importable
│   ├── client.py          # Groq client configuration
│   └── tools.py           # Shared tools like Search
├── .env                   # 🛑 API Keys (Git Ignored)
├── .env-sample            # 📄 Sample environment variables
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
```

---

## 🛠️ Building Agents
The repository will be structured into progressive complexity levels, for example:
- 01_simple_reflex/: Basic Chatbot (No memory, No tools)
- 02_tool_user/: Agent that can search the web or calculate
- 03_autonomous/: Agent that can plan and execute multiple steps.  
_(and more to follow)_

---

## 🏗️ Running with Docker

This project is containerized to ensure a consistent environment across different machines. Each agent has its own `Dockerfile`, but they are orchestrated from the root using **Docker Compose**.

### Using Profiles
To avoid launching all agents at once, we use **Docker Profiles**. You must specify which agent (or level) you want to run.

```bash
# Run a specific agent(s) by its profile
docker compose --profile level1 up

# Run multiple profiles at once
docker compose --profile level1 --profile level2 up

# Force a rebuild of the images
docker compose --profile level1 up --build
```

### Why Docker in this Monorepo?
1. **Isolated Environments**: Different agents can have different dependencies without conflicts.
2. **Shared Logic**: Docker correctly maps the `common/` utilities folder into each agent's container.
3. **Interactive Mode**: The configuration ensures you can still interact with the agents via the terminal (`stdin_open` and `tty`).

---

## 📚 Learning Resources

- [Groq Documentation](https://docs.groq.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain.com/langgraph)
- [CrewAI Documentation](https://docs.crewai.com/)

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request.

---

## 📧 Contact

Debmalya Pal

Project Link: [https://github.com/debmalyapal/ai-agents-foundation-101](https://github.com/debmalyapal/ai-agents-foundation-101)
