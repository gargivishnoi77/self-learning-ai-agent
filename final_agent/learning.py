from memory import (
    get_relevant_memory,
    load_memory
)


# ==========================================
# STRATEGY REPORT
# ==========================================

def strategy_report(task):

    relevant = get_relevant_memory(
        task
    )

    report = {}

    for experience in relevant:

        tool = experience.get(
            "tool"
        )

        if not tool:
            continue

        item = report.setdefault(
            tool,
            {
                "success": 0,
                "failed": 0,
                "retried": 0
            }
        )

        if experience.get(
            "success",
            False
        ):
            item["success"] += 1
        else:
            item["failed"] += 1

        if experience.get(
            "retried",
            False
        ):
            item["retried"] += 1

    for item in report.values():

        total = (
            item["success"]
            + item["failed"]
        )

        item["success_rate"] = (
            item["success"] / total
            if total
            else 0
        )

    return report


# ==========================================
# GLOBAL LEARNING REPORT
# ==========================================

def learning_report():

    memory = load_memory()

    if not memory:

        return {
            "total_experiences": 0,
            "successful": 0,
            "failed": 0,
            "success_rate": 0,
            "tools": {}
        }

    successful = sum(
        1
        for item in memory
        if item.get(
            "success",
            False
        )
    )

    failed = (
        len(memory)
        - successful
    )

    tools = {}

    for item in memory:

        tool = item.get(
            "tool",
            "unknown"
        )

        if tool not in tools:

            tools[tool] = {
                "success": 0,
                "failed": 0
            }

        if item.get(
            "success",
            False
        ):

            tools[tool]["success"] += 1

        else:

            tools[tool]["failed"] += 1

    return {

        "total_experiences":
            len(memory),

        "successful":
            successful,

        "failed":
            failed,

        "success_rate":
            successful / len(memory),

        "tools":
            tools
    }