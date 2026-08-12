<div align="center">

# <a href="https://github.com/Justt-Abhayyy/CodeScribe">CodeScribe</a>

### AI-Powered Codebase Documentation Agent

<p>
  <i>Understand your codebase, build structured context, and automatically generate professional documentation.</i>
</p>

<br>

[![GitHub Stars](https://img.shields.io/github/stars/Justt-Abhayyy/CodeScribe?style=flat\&color=ffd700)](https://github.com/Justt-Abhayyy/CodeScribe/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/Justt-Abhayyy/CodeScribe?style=flat\&color=red)](https://github.com/Justt-Abhayyy/CodeScribe/issues)
[![GitHub Forks](https://img.shields.io/github/forks/Justt-Abhayyy/CodeScribe?style=flat\&color=green)](https://github.com/Justt-Abhayyy/CodeScribe/network/members)
[![GitHub License](https://img.shields.io/github/license/Justt-Abhayyy/CodeScribe?style=flat\&color=blue)](https://github.com/Justt-Abhayyy/CodeScribe/blob/main/LICENSE)

</div>

---

## 🚀 What is CodeScribe?

**CodeScribe** is an AI-powered developer tool that analyzes software repositories and automatically generates clear, structured, and professional project documentation.

Instead of manually reading hundreds or thousands of lines of source code to understand a project, CodeScribe scans the repository, builds structured context for individual files, compresses that information into meaningful summaries, and uses those summaries to generate a comprehensive `README.md`.

The project is designed around a simple idea:

> **Better context produces better AI output.**

CodeScribe therefore focuses not only on documentation generation, but also on **context engineering for AI agents**.

---

## 🧠 Why CodeScribe?

Large software projects can contain hundreds of files, dependencies, configuration files, utilities, services, and interconnected components.

Giving an AI model the entire repository at once can result in:

* Excessive context usage
* Missing important information
* Irrelevant information overwhelming useful information
* Hallucinated project details
* Poorly structured documentation
* Expensive and inefficient inference

CodeScribe approaches the problem differently.

Instead of asking an AI model to understand the entire repository in one pass, it breaks the problem into smaller, focused stages.

```text
                    ┌─────────────────┐
                    │   Source Code   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Repository Scan │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ File Summaries  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Context Cache   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Final Synthesis │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   README.md     │
                    └─────────────────┘
```

---

# 🔬 Context Engineering

One of the main goals of CodeScribe is to explore practical techniques for building reliable AI agents that operate on real-world codebases.

The project is inspired by research and practical discussions around **advanced context engineering for coding agents**.

The central principle is straightforward:

> **The quality of the context provided to an AI system strongly influences the quality of its output.**

CodeScribe applies this principle throughout its documentation pipeline.

---

## 1. Stateless LLMs — Input Quality Matters

Large language models do not automatically retain knowledge about an entire repository.

Every inference call depends heavily on the information supplied to it.

CodeScribe therefore treats each stage of the pipeline as a **context construction problem**.

Instead of sending an entire repository to one model call, the system creates focused inputs for each stage.

### CodeScribe approach

```text
Raw Source Code
      ↓
Focused File Context
      ↓
Dense File Summary
      ↓
Structured Project Context
      ↓
Final Documentation
```

This allows each inference step to work with information that is relevant to its specific task.

---

## 2. Frequent Intentional Compaction

As an AI system works with a large codebase, the amount of intermediate information can grow quickly.

Too much information can reduce the quality of the final result.

CodeScribe addresses this through **intentional context compaction**.

A large source file can be transformed into a short, information-dense summary.

For example:

```text
500 lines of source code
          ↓
3–4 sentences of structured information
```

The resulting summary can then be reused instead of repeatedly sending the original source code into later inference stages.

This reduces context usage while preserving important information about the project.

---

## 3. Research → Plan → Implement

CodeScribe follows a staged workflow inspired by agentic software-engineering patterns.

### Research

The system first discovers the repository structure and identifies the files that need to be processed.

```text
Repository
    ↓
File discovery
    ↓
Project manifest
```

### Process

Individual files are processed independently and converted into structured summaries.

```text
Source File
    ↓
AI summarization
    ↓
Structured summary
```

### Synthesis

The collected summaries are combined and supplied to the final documentation stage.

```text
File summaries
      ↓
Project context
      ↓
AI synthesis
      ↓
README.md
```

Separating these stages prevents the final generation step from being overwhelmed by raw source code.

---

## 4. Context Isolation

CodeScribe processes individual files through bounded AI inference steps.

Each file can be understood independently before its information is passed into the larger documentation pipeline.

This provides several advantages:

* Smaller context windows
* Focused inference
* Reduced noise
* Better scalability
* Easier debugging
* Reusable intermediate summaries

Rather than asking one AI call to understand an entire repository, CodeScribe distributes the understanding process across multiple focused stages.

---

## 5. Prompts as Engineering Artifacts

AI prompts are an important part of CodeScribe's architecture.

The prompts define:

* What information the model should extract
* What information should be ignored
* How summaries should be structured
* How project context should be represented
* How the final README should be generated

This means prompts should be treated similarly to source code:

```text
Prompt
  ↓
Model Input
  ↓
Generated Output
```

A poor prompt can produce poor documentation even when the underlying model is capable.

CodeScribe therefore keeps its prompts version-controlled and treats them as an important part of the system.

---

# 🎯 Core Architecture

CodeScribe uses a multi-stage documentation pipeline.

| Stage              | Responsibility                                |
| ------------------ | --------------------------------------------- |
| Repository Scanner | Discovers project files                       |
| Context Manifest   | Defines files to process                      |
| File Processor     | Extracts relevant source information          |
| AI Summarizer      | Generates compact file summaries              |
| Context Cache      | Stores processed information                  |
| Final Synthesizer  | Combines summaries into project documentation |
| README Generator   | Produces the final `README.md`                |

---

# 📊 Context Engineering Principles

| Principle                   | CodeScribe Implementation                                      |
| --------------------------- | -------------------------------------------------------------- |
| Input quality matters       | Structured context is created before every AI call             |
| Intentional compaction      | Raw files are converted into dense summaries                   |
| Persistent context          | Processed summaries are cached                                 |
| Context isolation           | Individual files are processed through bounded inference calls |
| Staged processing           | Repository discovery → summarization → synthesis               |
| Minimize context usage      | Raw source is not unnecessarily passed to final generation     |
| Prompts as source artifacts | Prompt files are version-controlled                            |
| Reviewable output           | Generated documentation can be inspected and refined           |

---

# 🚀 Getting Started

## Prerequisites

Before installing CodeScribe, make sure you have:

* Python installed
* Git installed
* A supported LLM API key
* A project you want to document

---

## 1. Clone the Repository

```bash
git clone https://github.com/Justt-Abhayyy/CodeScribe.git
cd CodeScribe
```

---

## 2. Install Dependencies

If you are using `pip`:

```bash
pip install -e .
```

If you are using `uv`:

```bash
uv sync
```

---

## 3. Configure Your API Key

CodeScribe requires an LLM API key to run its AI documentation pipeline.

### Windows PowerShell

```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

### Windows CMD

```cmd
set GROQ_API_KEY=your_api_key_here
```

### Linux / macOS

```bash
export GROQ_API_KEY="your_api_key_here"
```

You can also place the key in a `.env` file if supported by your configuration.

**Never commit API keys or `.env` files containing secrets to GitHub.**

---

# 📖 CLI Usage

CodeScribe provides commands for initializing a project, configuring the AI model, running the documentation pipeline, and refreshing individual pieces of project context.

---

## `codescribe init`

### Initialize a project

Scans the repository and creates the project context manifest.

```bash
codescribe init
```

The initialization process:

* Scans the project directory
* Respects `.gitignore` rules
* Identifies files that should be processed
* Creates the project manifest
* Prepares cache and logging infrastructure
* Preserves existing model configuration

Run this command when starting CodeScribe on a new project or when the project structure changes significantly.

---

## `codescribe models`

### Discover available models

```bash
codescribe models
```

This command can be used to discover available AI models and their relevant context and output limits.

Choose a model based on the size and complexity of your project.

---

## `codescribe set default`

### Configure the default model

```bash
codescribe set default llama-3.3-70b-versatile
```

This sets the model used for future CodeScribe runs.

---

## `codescribe run`

### Generate project documentation

```bash
codescribe run
```

The command executes the complete documentation pipeline.

### Stage 1 — File Processing

Each relevant source file is processed individually.

```text
Source File
     ↓
AI Analysis
     ↓
Dense Summary
     ↓
Cache
```

### Stage 2 — Documentation Synthesis

The cached summaries are combined into a structured project context.

```text
Cached Summaries
       ↓
Project Context
       ↓
AI Synthesis
       ↓
README.md
```

---

## Override the Model

You can specify a model for an individual run:

```bash
codescribe run --model qwen/qwen3-32b
```

This allows you to experiment with different models without permanently changing your configuration.

---

# 🔄 Updating Project Context

When a project changes, you do not necessarily need to process the entire repository again.

CodeScribe supports targeted context updates.

### Update a specific file

```bash
codescribe update src/database/connection.py
```

This invalidates and recomputes the relevant cached information.

### Regenerate from existing context

```bash
codescribe update .
```

This can regenerate the documentation using the current cached project context without unnecessarily reprocessing every file.

---

# ⚙️ Configuration

CodeScribe uses a project configuration file to describe the project and its processing configuration.

Example:

```yaml
project: My Awesome Project

structure:
  - src/main.py
  - src/utils/helpers.py

llm:
  model: llama-3.3-70b-versatile
```

The `structure` section acts as the project's **context manifest**.

Instead of blindly processing every file, CodeScribe can use an explicit set of files that are relevant to understanding the project.

---

# 🗂️ Project Structure

A typical CodeScribe project contains components similar to:

```text
CodeScribe/
│
├── .github/
│   └── workflows/
│
├── CodeScribe/
│   ├── components/
│   ├── config/
│   ├── pipelines/
│   ├── prompts/
│   ├── resources/
│   ├── schema/
│   └── utils/
│
├── main.py
├── pyproject.toml
├── uv.lock
├── README.md
├── LICENSE
└── .gitignore
```

The internal structure may evolve as CodeScribe develops.

---

# 💡 Example Workflow

Suppose you have a project:

```text
MyProject/
├── src/
├── tests/
├── config/
├── requirements.txt
└── README.md
```

Run:

```bash
codescribe init
```

Then:

```bash
codescribe run
```

CodeScribe analyzes the project and produces documentation based on the information it extracts.

Conceptually:

```text
MyProject
    │
    ├── Source files
    ├── Configuration
    ├── Utilities
    └── Dependencies
            │
            ▼
      CodeScribe Scanner
            │
            ▼
      File-level Analysis
            │
            ▼
      Context Cache
            │
            ▼
      Project Synthesis
            │
            ▼
        README.md
```

---

# ✨ Key Features

### 🤖 AI-Powered Analysis

Uses LLM inference to understand source code and generate meaningful project documentation.

### 🧩 Multi-Stage Processing

Breaks documentation generation into smaller, focused processing stages.

### 🧠 Context Engineering

Designed around structured context construction rather than simply sending an entire repository to an AI model.

### ⚡ Efficient Processing

Caches intermediate summaries so previously processed information can be reused.

### 🔄 Selective Updates

Allows specific files or directories to be refreshed without rebuilding the entire context.

### 📝 Automatic README Generation

Produces a structured project README based on the AI's understanding of the repository.

### 🛠️ CLI-Based Workflow

Designed to work directly from the command line and integrate naturally with developer workflows.

---

# 🧪 Experiments & Future Improvements

Potential areas for extending CodeScribe include:

* Cross-file dependency analysis
* Retrieval-augmented documentation generation
* Parallel file summarization
* Improved cache invalidation
* Multi-language support
* Documentation templates
* Architecture diagram generation
* API documentation generation
* Code dependency graphs
* Better error recovery and retry handling
* Local LLM support
* Documentation quality evaluation
* Automated documentation updates through CI/CD

---

# 🤝 Contributing

Contributions and experiments are welcome.

Some useful areas for contribution include:

### Prompt Engineering

Improve the quality and reliability of generated documentation.

### Context Pipeline

Experiment with:

* Cross-file context
* Retrieval
* Structured intermediate representations
* Context compression
* Agent isolation

### Reliability

Potential improvements include:

* Retry mechanisms
* Atomic cache updates
* Better error handling
* Parallel processing
* Improved logging

### Language Support

Extend CodeScribe beyond Python to ecosystems such as:

* JavaScript
* TypeScript
* Java
* Go
* Rust
* C++
* C#

---

# 🐛 Issues & Feedback

Found a bug or generated documentation that does not accurately represent your project?

Open an issue:

👉 https://github.com/Justt-Abhayyy/CodeScribe/issues

When reporting an issue, include:

* The command you executed
* Relevant configuration
* Terminal output
* The generated documentation
* The expected behavior

This makes it easier to reproduce and diagnose problems.

---

# 📜 License

CodeScribe is distributed under the **GNU AGPLv3 License**.

See the [`LICENSE`](LICENSE) file for details.

---

# ⭐ Support the Project

If CodeScribe is useful to you, consider giving the repository a ⭐ on GitHub.

**Repository:**
https://github.com/Justt-Abhayyy/CodeScribe

---

<div align="center">

### CodeScribe

**Turn codebases into understandable documentation.**

</div>
