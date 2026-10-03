# Self-Learning AI Agent

A modular AI agent built in Python that can **plan tasks, select specialized tools, evaluate results, learn from previous executions, and reuse successful strategies**.

The project demonstrates how an agent can move beyond simple chatbot behavior by combining planning, tool execution, evaluation, reflection, persistent memory, and strategy reuse.

---

## 🚀 Project Overview

The agent accepts a natural-language task and determines how it should be solved.

Instead of relying on a single fixed workflow, it can:

- Understand the task type
- Create an execution plan
- Select an appropriate tool
- Execute the task
- Evaluate the result
- Reflect when an attempt fails
- Retry using an alternative strategy
- Store the experience in persistent memory
- Reuse successful strategies on future tasks

### Core Idea

```text
                    User Task
                       │
                       ▼
                ┌──────────────┐
                │ Task Planner │
                └──────┬───────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Strategy Select │
              └────────┬────────┘
                       │
                       ▼
                ┌─────────────┐
                │ Tool Execute│
                └──────┬──────┘
                       │
                       ▼
                 ┌───────────┐
                 │ Evaluator │
                 └─────┬─────┘
                       │
                 ┌─────┴─────┐
                 │           │
              Success      Failure
                 │           │
                 │      ┌─────▼─────┐
                 │      │ Reflection│
                 │      └─────┬─────┘
                 │            │
                 │          Retry
                 │            │
                 └──────┬─────┘
                        ▼
                 ┌─────────────┐
                 │    Memory   │
                 └──────┬──────┘
                        │
                        ▼
                 Learned Strategy
````

---

## ✨ Features

### 1. Task Planning

The agent identifies the type of task and creates an appropriate execution plan.

Supported task categories include:

* Arithmetic
* Word counting
* Multi-step tasks
* Research
* Coding
* File operations
* Data analysis

---

### 2. Specialized Tools

The agent uses different tools depending on the task.

| Tool                    | Purpose                       |
| ----------------------- | ----------------------------- |
| `calculator`            | Basic arithmetic              |
| `expression_calculator` | Safe mathematical expressions |
| `word_counter`          | Count words in text           |
| `research_tool`         | Retrieve research information |
| `coding_tool`           | Handle supported coding tasks |
| `file_tool`             | Work with local project files |
| `data_tool`             | Analyze CSV and JSON data     |

This modular design makes it possible to add new capabilities without redesigning the entire agent.

---

### 3. Multi-Step Task Execution

The agent can break a task into multiple steps and pass information between them.

Example:

```text
Calculate 10 % 3
        ↓
Result = 1
        ↓
Count words in "learning agents improve"
        ↓
Result = 3
        ↓
Overall task = Successful
```

The agent maintains execution context so later steps can use previous results.

---

### 4. Evaluation

Every tool execution is evaluated to determine whether it succeeded.

```text
Tool Execution
      ↓
    Result
      ↓
   Evaluator
      ↓
Success / Failure
```

This provides the feedback signal required for learning and retry behavior.

---

### 5. Reflection & Retry

When an execution fails, the agent can reflect on the failure and attempt an alternative strategy.

Example:

```text
Task
 ↓
Initial Strategy
 ↓
Failure
 ↓
Reflection
 ↓
Alternative Strategy
 ↓
Retry
 ↓
Success
```

The retry mechanism is intentionally controlled rather than allowing unlimited attempts.

---

### 6. Persistent Memory

The agent stores previous experiences in `memory.json`.

Stored information includes:

* Task
* Task type
* Tool used
* Result
* Success/failure
* Retry information
* Execution context
* Timestamp

This allows the agent to use previous experience when handling future tasks.

> `memory.json` is intentionally excluded from Git because it contains runtime-generated experience data.

---

### 7. Strategy Reuse

The strategy selector searches previous experiences for successful strategies that are compatible with the current task.

For example:

```text
Previous Experience

Modulo task
     ↓
calculator → failed
     ↓
expression_calculator → successful


Future Modulo Task
        ↓
Memory
        ↓
expression_calculator
        ↓
Success
```

This is the main mechanism behind the project's **self-learning behavior**.

---

### 8. Optional LLM Planning

The project also contains an optional LLM planner.

The local planner can operate without an API key, while the LLM planner can be enabled when API access is available.

This keeps the core agent usable even without an external LLM service.

---

# 🧠 Architecture

The project follows a modular architecture:

```text
                      ┌──────────────┐
                      │     User     │
                      └──────┬───────┘
                             ↓
                      ┌──────────────┐
                      │    Planner   │
                      └──────┬───────┘
                             ↓
                   ┌──────────────────────┐
                   │ Strategy Selection   │
                   └──────────┬───────────┘
                              ↓
                      ┌───────────────┐
                      │ Tool Registry │
                      └───────┬───────┘
                              ↓
                ┌─────────────────────────┐
                │      Tool Execution     │
                │                         │
                │ Calculator              │
                │ Research                │
                │ Coding                  │
                │ Files                   │
                │ Data                    │
                │ Word Counter            │
                └────────────┬────────────┘
                             ↓
                      ┌─────────────┐
                      │  Evaluator  │
                      └──────┬──────┘
                             ↓
                      ┌─────────────┐
                      │ Reflection  │
                      └──────┬──────┘
                             ↓
                      ┌─────────────┐
                      │   Memory    │
                      └──────┬──────┘
                             ↓
                      Strategy Reuse
```

---

# 📁 Project Structure

```text
self-learning-ai-agent/
│
├── final_agent/
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
│   ├── README.md
│   ├── .env.example
│   └── .gitignore
│
├── .gitignore
└── README.md
```

---

# 🛠️ Technologies

* **Python**
* **OpenAI API** — optional LLM planning
* **Python AST** — safe mathematical expression evaluation
* **JSON** — persistent memory
* **CSV** — data analysis
* **urllib** — research requests
* **Git & GitHub** — version control

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/gargivishnoi77/self-learning-ai-agent.git
cd self-learning-ai-agent
```

Create and activate a virtual environment:

### Windows

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install dependencies:

```powershell
pip install openai python-dotenv
```

Move into the agent directory:

```powershell
cd final_agent
```

---

# ▶️ Run the Agent

Start the interactive agent:

```powershell
python main.py
```

You can enter tasks such as:

```text
Calculate 25 + 75
```

```text
Count words artificial intelligence agents
```

```text
Calculate 10 % 3 and then count words learning agents improve
```

```text
Write a Python function to reverse a string
```

```text
Research machine learning
```

---

# 🧪 Benchmark

The project includes a benchmark containing **10 different tasks** covering multiple capabilities.

The benchmark tests:

* Arithmetic
* Modulo
* Division
* Word counting
* Multi-step execution
* Coding
* File operations
* Research
* Data analysis

The benchmark was executed twice:

```text
                 First Pass    Second Pass
Successful           10/10         10/10
Failed                0/10          0/10
Success Rate        100%          100%
```

The second pass was specifically used to validate **strategy reuse from previous experience**.

### Validation Result

```text
First pass success rate:   100%
Second pass success rate:  100%

Learning / reuse validation: PASSED
```

The benchmark also generated persistent agent experiences that were used by the strategy-selection system during subsequent executions.

---

# 🔄 Learning Workflow

The agent's learning loop can be summarized as:

```text
Task
 ↓
Plan
 ↓
Select Strategy
 ↓
Execute Tool
 ↓
Evaluate
 ↓
 ┌───────────────┐
 │               │
Success        Failure
 │               │
 ↓               ↓
Store          Reflect
Experience       ↓
 │             Retry
 └───────┬───────┘
         ↓
      Memory
         ↓
  Strategy Reuse
```

The system therefore does not simply execute tasks independently. Previous execution outcomes influence future strategy selection.

---

# 🔐 Security & Design Considerations

The project uses several safeguards for local execution:

* Mathematical expressions are parsed using Python's AST rather than unrestricted `eval`.
* File operations are restricted to the project directory.
* `.env` files are excluded from Git.
* Virtual environments are excluded from Git.
* Runtime memory is excluded from Git.
* Retry attempts are limited to avoid uncontrolled execution loops.

---

# 📌 Current Status

**V6 Core — Validated**

Current implementation includes:

* Task planning
* Specialized tools
* Multi-step execution
* Execution context
* Evaluation
* Reflection
* Controlled retry
* Persistent memory
* Strategy selection
* Strategy reuse
* Benchmarking
* Optional LLM planning

---

# 🚧 Limitations

The current version is intentionally focused on demonstrating the agent architecture rather than being a general-purpose autonomous system.

Current limitations include:

* The local planner uses predefined task patterns.
* The available tools are limited to the implemented tool registry.
* LLM planning is optional and depends on API availability.
* Research functionality depends on network access.
* Coding capabilities currently cover supported local coding tasks rather than arbitrary software development.
* Learning is based on stored execution experiences rather than model parameter updates.

---

# 🔮 Future Improvements

Possible future extensions include:

* More advanced task decomposition
* Additional specialized tools
* Improved LLM-based planning
* More sophisticated experience retrieval
* Experiment-based strategy selection
* Long-term memory improvements
* Agent performance dashboard
* Specialized research and coding agents
* More extensive evaluation benchmarks

---

# 🎯 Project Goal

The goal of this project is to explore how **planning, tools, evaluation, memory, reflection, and strategy reuse can be combined to create an AI agent that improves its task-solving behavior through experience.**

Rather than building another chatbot, this project focuses on the **agentic workflow behind task execution and learning**.

---

## 👩‍💻 Author

**Gargi Vishnoi**

B.Tech — Computer Science & Artificial Intelligence

GitHub: [@gargivishnoi77](https://github.com/gargivishnoi77)

---

## 📄 License

This project is intended as a learning and portfolio project.