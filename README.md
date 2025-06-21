# Code Reviewer Agent 🤖

> **Study Project**: This project was created as a learning experience to explore modern development practices and AI agent workflows.

## 📚 Learning Objectives

This project served as a comprehensive study to learn:

- **GitHub Actions & Workflows** 🔄 - Automated CI/CD pipelines
- **uv Package Manager** ⚡ - Modern Python dependency management
- **LangChain Framework** 🧠 - Building AI agent workflows
- **AI-Powered Code Review** 🔍 - Automated code analysis

## 🎯 Project Overview

An intelligent AI agent that automatically reviews code changes using LangChain framework. The agent analyzes git diffs, provides contextual feedback, and generates comprehensive code review reports.

## 🏗️ Architecture

The project follows a modular agent-based architecture:

```
code-reviewer-agent/
├── cli.py                    # Command-line interface
├── code_reviewer/
│   ├── agents/
│   │   ├── diff_reader.py    # Extracts git diffs
│   │   ├── context_analyst.py # Analyzes code context
│   │   ├── change_critic.py  # AI-powered code review
│   │   └── report_writer.py  # Generates review reports
│   ├── llm_interface.py      # LLM provider abstraction
│   └── pipeline.py           # Orchestrates the workflow
└── .github/workflows/        # GitHub Actions automation
```

## 🚀 Features

- **Automated Code Review**: Triggers on PR creation/updates
- **Multi-LLM Support**: OpenAI and Ollama integration
- **Context-Aware Analysis**: Full source code context consideration
- **Structured Output**: JSON-formatted review comments
- **Severity Classification**: Info, Warning, Critical levels
- **GitHub Integration**: Direct PR commenting and also commit commenting if Personal Access Token is defined.

## 🔧 Setup & Installation

### Prerequisites

- Python 3.10+
- Git repository access
- LLM API access (OpenAI for getting PR/Commits comments in GutHub using Workflow or Ollama for running Local and generating MarkDown Report)

### Installation

```bash
# Clone the repository
git clone https://github.com/JPVercosa/code-reviewer-agent.git
cd code-reviewer-agent

# Install using uv (recommended)
uv sync

# Or install system-wide
uv pip install --system .
```

### Usage

```bash
# Run code review on a repository
python cli.py --repo /path/to/your/repo
```

## 🔐 Environment Secrets

### Required Secrets

The following environment variables must be configured:

#### For OpenAI Integration and using with Workflow

```bash
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini  # or gpt-4o, gpt-3.5-turbo
```

#### For Ollama Integration and running locally generating MardDown report

```bash
LLM_PROVIDER=ollama
LLM_MODEL=qwen3:8b-q4_K_M  # or any local model
OLLAMA_BASE_URL=http://localhost:11434  # optional, defaults to localhost
```

#### For GitHub Actions

```bash
GITHUB_TOKEN=your_github_token
PAT_FOR_COMMENTS=your_personal_access_token  # necessery to allow commits commenting
```

### Optional Configuration

```bash
LLM_TEMPERATURE=0.1  # Controls response creativity (0.0-1.0)
```

## 🔄 GitHub Actions Workflow

The project includes automated GitHub Actions that:

1. **Triggers**: On push to main or PR events
2. **Setup**: Installs Python 3.12 and uv package manager
3. **Installation**: Installs the code reviewer agent system-wide
4. **Execution**: Runs the agent on the target repository
5. **Integration**: Posts review comments directly to PRs

### Workflow File: `.github/workflows/code_review.yml`

## 🧪 Testing

```bash
# Test with sample repository
python cli.py --repo tests/sample_repo
```

## 🎓 What I Learned

### GitHub Actions & Workflows

- Setting up automated CI/CD pipelines
- Managing secrets and environment variables
- Cross-repository actions
- Conditional job execution
- Artifact management

### uv Package Manager

- Modern Python dependency resolution
- Fast package installation
- Virtual environment management
- Lock file generation

### LangChain Framework

- Building modular AI agent workflows
- LLM provider abstraction
- Prompt engineering and templates
- Output parsing and validation
- Chain composition and orchestration

### AI Agent Development

- Multi-agent architecture design
- Context-aware processing
- Error handling and fallbacks
- Structured output generation
- Integration with external APIs

## 🤝 Contributing

This is a study project, but contributions are welcome! Feel free to:

- Report bugs
- Suggest improvements
- Add new LLM providers
- Enhance the review logic

## 📄 License

This project is open source and available under the MIT License.

---

_Built with ❤️ as a learning experience in modern AI development practices_
