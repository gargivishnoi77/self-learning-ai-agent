import json
import os
from datetime import datetime


MEMORY_FILE = "memory.json"


# ==========================================
# TASK TYPE
# ==========================================

def get_task_type(task):

    text = task.lower().strip()

    if " and then " in text:
        return "multi_step"

    if (
        "research" in text
        or "search" in text
        or "look up" in text
    ):
        return "research"

    if (
        "write code" in text
        or "python function" in text
        or "coding" in text
        or "code" in text
        or "debug" in text
    ):
        return "coding"

    if (
        "read file" in text
        or "open file" in text
        or "list files" in text
        or "find in file" in text
    ):
        return "file"

    if (
        "csv" in text
        or "json" in text
        or "dataset" in text
        or "analyze data" in text
        or "analyse data" in text
    ):
        return "data"

    if "count words" in text:
        return "word_count"

    if "%" in text or "remainder" in text:
        return "modulo"

    if "+" in text:
        return "addition"

    if " - " in text:
        return "subtraction"

    if "*" in text:
        return "multiplication"

    if " / " in text:
        return "division"

    if "calculate" in text:
        return "calculation"

    return "general"


# ==========================================
# LOAD MEMORY
# ==========================================

def load_memory():

    if not os.path.exists(
        MEMORY_FILE
    ):
        return []

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception:

        return []


# ==========================================
# SAVE MEMORY
# ==========================================

def save_memory(
    task,
    tool,
    result,
    success,
    retried=False,
    context=None
):

    memory = load_memory()

    experience = {

        "task": task,

        "task_type":
            get_task_type(task),

        "tool": tool,

        "result": str(result),

        "success":
            bool(success),

        "retried":
            bool(retried),

        "context":
            context,

        "timestamp":
            datetime.now().isoformat()
    }

    memory.append(experience)

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# RELEVANT MEMORY
# ==========================================

def get_relevant_memory(task):

    task_type = get_task_type(task)

    return [
        experience
        for experience in load_memory()
        if experience.get(
            "task_type"
        ) == task_type
    ]


# ==========================================
# SUCCESSFUL EXPERIENCES
# ==========================================

def get_successful_experiences(task):

    return [
        experience
        for experience in get_relevant_memory(task)
        if experience.get(
            "success",
            False
        )
    ]


# ==========================================
# BEST PREVIOUS STRATEGY
# ==========================================

def get_best_previous_strategy(task):

    experiences = (
        get_successful_experiences(task)
    )

    if not experiences:
        return None

    statistics = {}

    for experience in experiences:

        tool = experience.get("tool")

        if not tool:
            continue

        statistics[tool] = (
            statistics.get(tool, 0) + 1
        )

    if not statistics:
        return None

    return max(
        statistics,
        key=statistics.get
    )