import re


# ==========================================
# TASK TYPE DETECTION
# ==========================================

def detect_task_type(task):

    text = task.lower().strip()

    # Multi-step must come first.
    if " and then " in text:
        return "multi_step"

    # Research
    research_words = [
        "research",
        "search",
        "find information",
        "look up",
        "what is",
        "who is",
        "explain"
    ]

    if any(
        word in text
        for word in research_words
    ):
        return "research"

    # Coding
    coding_words = [
        "write code",
        "write a python",
        "python function",
        "coding",
        "code",
        "program",
        "debug"
    ]

    if any(
        word in text
        for word in coding_words
    ):
        return "coding"

    # File
    file_words = [
        "read file",
        "open file",
        "list files",
        "find in file",
        "search file"
    ]

    if any(
        word in text
        for word in file_words
    ):
        return "file"

    # Data
    data_words = [
        "csv",
        "json",
        "dataset",
        "analyze data",
        "analyse data",
        "analyze dataset",
        "analyse dataset"
    ]

    if any(
        word in text
        for word in data_words
    ):
        return "data"

    # Existing tools
    if "count words" in text:
        return "word_count"

    if "%" in text or "remainder" in text:
        return "modulo"

    if "*" in text:
        return "multiplication"

    if " / " in text or "divide" in text:
        return "division"

    if " - " in text:
        return "subtraction"

    if " + " in text:
        return "addition"

    if "calculate" in text:
        return "calculation"

    return "general"


# ==========================================
# EXPRESSION EXTRACTION
# ==========================================

def extract_expression(task):

    text = task.lower().strip()

    text = text.replace(
        "calculate",
        "",
        1
    ).strip()

    match = re.search(
        r"(\d+(?:\.\d+)?)\s+"
        r"(?:divided by|/)\s+"
        r"(\d+(?:\.\d+)?)",
        text
    )

    if match:

        return (
            f"{match.group(1)} / "
            f"{match.group(2)}"
        )

    return text


# ==========================================
# SINGLE TASK PLANNER
# ==========================================

def plan_single_task(task):

    task_type = detect_task_type(task)

    tool_map = {

        "word_count":
            "word_counter",

        "modulo":
            "expression_calculator",

        "addition":
            "calculator",

        "subtraction":
            "calculator",

        "multiplication":
            "calculator",

        "division":
            "calculator",

        "calculation":
            "expression_calculator",

        "research":
            "research_tool",

        "coding":
            "coding_tool",

        "file":
            "file_tool",

        "data":
            "data_tool"
    }

    tool = tool_map.get(
        task_type,
        "none"
    )

    return {
        "tool": tool,
        "task": task
    }


# ==========================================
# LOCAL PLANNER
# ==========================================

def plan_task(task):

    text = task.lower().strip()

    if " and then " in text:

        parts = task.split(
            " and then "
        )

        return [
            plan_single_task(
                part.strip()
            )
            for part in parts
        ]

    return [
        plan_single_task(task)
    ]