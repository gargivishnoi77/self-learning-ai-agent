# Self-Learning AI Agent

A modular AI agent that can plan tasks, select appropriate tools, evaluate results, remember previous experiences, reflect on failures, and reuse successful strategies on future tasks.

This project explores how an AI agent can go beyond a basic chatbot by planning tasks, using tools, evaluating results, storing previous experiences, and reusing successful strategies..

---

## 🚀 Overview

The Self-Learning AI Agent accepts a natural-language task and determines how to solve it.

Instead of using a single fixed workflow, the agent can:

* Understand the type of task
* Create an execution plan
* Select an appropriate tool
* Execute the task
* Evaluate the result
* Store the experience in persistent memory
* Reflect and retry when necessary
* Learn which strategies work for different task types
* Reuse successful strategies on future tasks

The project also supports optional LLM-based planning. When an API key is unavailable, the system falls back to its local planning system.

---

## 🧠 Core Architecture

```text
                    USER TASK
                        │
                        ▼
                 ┌──────────────┐
                 │ Task Planner │
                 └──────┬───────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Strategy Selector │
              └─────────┬─────────┘
                        │
                        ▼
                ┌───────────────┐
                │   Tool Layer  │
                └───────┬───────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     Calculator      Research       Coding
          │             │             │
          ├─────────────┼─────────────┤
          ▼             ▼             ▼
       Files           Data       Word Counter
                        │
                        ▼
                 ┌────────────┐
                 │  Evaluator │
                 └─────┬──────┘
                       │
              ┌────────┴────────┐
              │                 │
           Success            Failure
              │                 │
              ▼                 ▼
         Save Memory       Reflection
              │                 │
              │                 ▼
              │               Retry
              │                 │
              └────────┬────────┘
                       ▼
              Persistent Memory
                       │
                       ▼
              Better Strategy
              for Future Tasks
```

## ✨ Features

### 1. Task Planning

The planner identifies the type of task and creates an appropriate execution plan.

Supported task categories include:

* Calculations
* Word counting
* Research
* Coding
* File operations
* Data analysis
* Multi-step tasks

---

### 2. Tool-Based Execution

The agent uses specialized tools instead of trying to solve every task through one method.

Current tools include:

| Tool                    | Purpose                                  |
| ----------------------- | ---------------------------------------- |
| `calculator`            | Basic arithmetic                         |
| `expression_calculator` | Safe mathematical expressions            |
| `word_counter`          | Counts words in text                     |
| `research_tool`         | Searches Wikipedia for information       |
| `coding_tool`           | Handles selected Python coding tasks     |
| `file_tool`             | Reads, lists, and searches project files |
| `data_tool`             | Analyzes CSV and JSON data               |

---

### 3. Multi-Step Task Execution

The agent can break a task into multiple steps and pass the result of one step into the next.

Example:

```text
Calculate 10 % 3 and then count words learning agents improve
```

The agent performs:

```text
Step 1 → Calculate 10 % 3
       → Result: 1

Step 2 → Count words learning agents improve
       → Result: 3
```

The previous result can also be provided as context for subsequent steps.

---

### 4. Persistent Memory

The agent stores previous experiences in:

```text
memory.json
```

Each experience can contain information such as:

* Task
* Task type
* Tool used
* Result
* Success/failure
* Retry information
* Context
* Timestamp

This allows the agent to use information from previous executions.

---

### 5. Strategy Selection

The strategy module analyzes previous experiences and selects compatible strategies for future tasks.

For example:

```text
Previous task
      ↓
Tool used
      ↓
Was it successful?
      ↓
Store experience
      ↓
Future similar task
      ↓
Reuse successful strategy
```

The system avoids blindly selecting a previously successful tool when that tool is incompatible with the current task type.

---

### 6. Reflection and Retry

When an execution fails, the agent can reflect on the result and attempt a controlled retry.

The current implementation limits retries to prevent uncontrolled execution loops.

```text
Task
 ↓
Execute
 ↓
Evaluate
 ↓
Failure?
 ↓
Reflection
 ↓
Retry
 ↓
Evaluate Again
```

---

### 7. Evaluator

The evaluator determines whether a tool execution produced an acceptable result.

This provides a feedback signal that can be stored in memory and used by the strategy-selection system.

---

### 8. Optional LLM Planning

The project includes an optional LLM planner.

If an OpenAI API key is available, the agent can use an LLM for planning.

If the API key is unavailable, the agent continues using the local planner.

This makes the core system usable without requiring an external LLM API.

---

## 🔄 How the Agent Learns

The learning process is based on previous execution experiences.

```text
             New Task
                 │
                 ▼
          Identify Task Type
                 │
                 ▼
       Check Previous Memory
                 │
                 ▼
       Select Compatible Tool
                 │
                 ▼
             Execute
                 │
                 ▼
             Evaluate
                 │
          ┌──────┴──────┐
          │             │
       Success        Failure
          │             │
          ▼             ▼
    Store Success    Reflect
          │             │
          │             ▼
          │           Retry
          │             │
          └──────┬──────┘
                 ▼
          Update Experience
                 │
                 ▼
       Future Strategy Reuse
```

The important idea is that the agent does not modify its underlying model weights. Instead, its improvement comes from **persistent experience, strategy selection, and reuse of successful approaches**.

---

## 📁 Project Structure

```text
self-learning-ai-agent-final/
│
├── final_agent/
│   │
│   ├── agent.py
│   ├── planner.py
│   ├── strategy.py
│   ├── memory.py
│   ├── learning.py
│   ├── reflection.py
│   ├── evaluator.py
│   ├── tools.py
│   ├── llm_planner.py
│   ├── benchmark.py
│   ├── main.py
│   │
│   ├── memory.json
│   ├── .env.example
│   ├── .gitignore
│   └── README.md
│
└── venv/
```

### Main Modules

**`agent.py`**
Core agent loop that coordinates planning, execution, evaluation, memory, reflection, and retries.

**`planner.py`**
Classifies tasks and creates local execution plans.

**`strategy.py`**
Selects compatible strategies based on previous successful experiences.

**`memory.py`**
Handles persistent experience storage and retrieval.

**`learning.py`**
Generates learning and strategy performance reports.

**`reflection.py`**
Provides reflection information used during retry.

**`evaluator.py`**
Evaluates execution results.

**`tools.py`**
Contains the agent's available tools.

**`llm_planner.py`**
Optional LLM-based planning component.

**`benchmark.py`**
Runs the validation benchmark and tests learning/reuse behavior.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd self-learning-ai-agent-final
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install openai python-dotenv
```

### 4. Configure the environment

Copy:

```text
.env.example
```

to:

```text
.env
```

Add your API key if you want to enable optional LLM planning.

Never commit `.env` or expose API keys publicly.

---

## ▶️ Running the Agent

Move into the agent directory:

```powershell
cd final_agent
```

Run:

```powershell
python main.py
```

You can then enter tasks such as:

```text
Calculate 25 + 75
```

or:

```text
Research machine learning
```

or:

```text
Write a Python function to reverse a string
```

or:

```text
Calculate 10 % 3 and then count words learning agents improve
```

---

## 🧪 Benchmark

The project includes a validation benchmark covering different capabilities:

* Arithmetic
* Expression evaluation
* Word counting
* Multi-step execution
* Coding
* File operations
* Research
* Data analysis
* Strategy reuse

Run:

```powershell
python benchmark.py
```

### Latest Validation Result

The V6 validation benchmark used **10 tasks per pass**.

| Metric                    |  Result |
| ------------------------- | ------: |
| First-pass success        | 10 / 10 |
| First-pass success rate   |    100% |
| Second-pass success       | 10 / 10 |
| Second-pass success rate  |    100% |
| Learning/reuse validation |  PASSED |

The second pass demonstrated that previously successful compatible strategies could be reused for subsequent executions.

The benchmark also exercised the research, coding, file, data, calculation, word-counting, and multi-step capabilities.

---

## 🧩 Design Principles

### Modular

Each major responsibility is separated into its own module.

### Tool-Based

Different task types can use specialized tools.

### Persistent

Experiences are stored beyond a single execution.

### Evaluated

Results are evaluated instead of assuming every tool execution succeeded.

### Reflective

Failures can trigger reflection and a controlled retry.

### Compatibility-Aware

Previously successful strategies are considered only when they are compatible with the current task.

### Fallback-Oriented

The agent can continue operating with local planning when the optional LLM planner is unavailable.

---

## ⚠️ Current Limitations

This project is a practical learning-oriented agent architecture and has several limitations.

* The LLM planner is optional and depends on API availability.
* The local planner is rule-based.
* The research tool currently uses Wikipedia.
* The coding tool contains built-in handling for selected coding tasks rather than being a general autonomous coding system.
* File and data operations are intentionally restricted to the local project environment.
* Persistent learning is based on stored experiences and strategy reuse rather than model fine-tuning.
* The benchmark demonstrates controlled task performance but is not a substitute for large-scale evaluation.

---

## 🔮 Future Improvements

Possible future extensions include:

* More advanced LLM-based planning
* Specialized research and coding agents
* Better task decomposition
* More robust failure analysis
* Experiment-based strategy selection
* Semantic memory retrieval
* Vector-based long-term memory
* More sophisticated evaluation metrics
* Web and API tools
* Agent monitoring dashboard
* Parallel tool execution
* Improved autonomous coding capabilities

---

## 🎯 Project Goal

The goal of this project is to understand and implement the fundamental components behind modern AI agents:

```text
Planning
   ↓
Tool Use
   ↓
Execution
   ↓
Evaluation
   ↓
Reflection
   ↓
Memory
   ↓
Strategy Selection
   ↓
Experience Reuse
```

Rather than building only a chatbot, this project focuses on creating an agent that can **use tools, evaluate its actions, remember experiences, and reuse successful strategies**.

---

## 🛠️ Technologies

* Python
* OpenAI API (optional)
* python-dotenv
* JSON
* CSV
* Wikipedia API
* Python AST
* Modular agent architecture

---

## 👩‍💻 Author

**Gargi Vishnoi**

B.Tech Computer Science & Artificial Intelligence

---

## 📌 Status

**V6 Core — Validated**

The core agent architecture, tool layer, memory system, strategy selection, reflection, controlled retry, multi-step execution, and benchmark validation are implemented.
