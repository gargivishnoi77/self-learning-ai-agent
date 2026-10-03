from memory import (
    get_relevant_memory,
    get_task_type
)


# ==========================================
# TOOL COMPATIBILITY
# ==========================================

COMPATIBLE_TOOLS = {

    "word_count": [
        "word_counter"
    ],

    "addition": [
        "calculator",
        "expression_calculator"
    ],

    "subtraction": [
        "calculator",
        "expression_calculator"
    ],

    "multiplication": [
        "calculator",
        "expression_calculator"
    ],

    "division": [
        "calculator",
        "expression_calculator"
    ],

    "modulo": [
        "expression_calculator"
    ],

    "calculation": [
        "expression_calculator",
        "calculator"
    ],

    "research": [
        "research_tool"
    ],

    "coding": [
        "coding_tool"
    ],

    "file": [
        "file_tool"
    ],

    "data": [
        "data_tool"
    ],

    "multi_step": [],

    "general": []
}


# ==========================================
# STRATEGY SELECTION
# ==========================================

def select_strategy(task):

    task_type = get_task_type(task)

    print(
        "Strategy Selector: "
        "Task type =",
        task_type
    )

    compatible = (
        COMPATIBLE_TOOLS.get(
            task_type,
            []
        )
    )

    if not compatible:

        print(
            "Strategy Selector: "
            "No known compatible strategy."
        )

        return None

    memory = get_relevant_memory(task)

    statistics = {}

    for experience in memory:

        tool = experience.get(
            "tool"
        )

        if tool not in compatible:
            continue

        if tool not in statistics:

            statistics[tool] = {
                "success": 0,
                "total": 0,
                "retry_success": 0
            }

        statistics[tool]["total"] += 1

        if experience.get(
            "success",
            False
        ):

            statistics[tool]["success"] += 1

            if experience.get(
                "retried",
                False
            ):
                statistics[tool][
                    "retry_success"
                ] += 1

    if not statistics:

        print(
            "Strategy Selector: "
            "No learned strategy found."
        )

        return None

    best_tool = None
    best_score = -1

    for tool in compatible:

        if tool not in statistics:
            continue

        stats = statistics[tool]

        success_rate = (
            stats["success"]
            / stats["total"]
        )

        score = (
            success_rate * 100
            + stats["success"] * 0.01
        )

        print(
            f"Strategy: {tool} | "
            f"Success rate: "
            f"{success_rate * 100:.2f}% "
            f"({stats['success']}/"
            f"{stats['total']})"
        )

        if score > best_score:

            best_score = score
            best_tool = tool

    if best_tool:

        print(
            "Strategy Selector: "
            "Best strategy for",
            task_type,
            "=",
            best_tool
        )

    return best_tool