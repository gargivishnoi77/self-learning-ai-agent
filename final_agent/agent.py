from planner import (
    plan_task,
    detect_task_type
)

from strategy import (
    select_strategy
)

from memory import (
    save_memory
)

from evaluator import (
    evaluate_result,
    evaluate_plan
)

from reflection import (
    reflect_on_failure
)

from llm_planner import (
    get_llm_plan
)

from tools import (
    calculator,
    expression_calculator,
    word_counter,
    research_tool,
    coding_tool,
    file_tool,
    data_tool
)


MAX_RETRIES = 1


# ==========================================
# AGENT CONTEXT
# ==========================================

class AgentContext:

    def __init__(self):

        self.results = []

    def add_result(
        self,
        step,
        task,
        tool,
        result
    ):

        self.results.append({

            "step":
                step,

            "task":
                task,

            "tool":
                tool,

            "result":
                result
        })

    def latest_result(self):

        if not self.results:
            return None

        return self.results[-1][
            "result"
        ]

    def get_context_text(self):

        if not self.results:
            return ""

        context = []

        for item in self.results:

            context.append(
                f"Step {item['step']} "
                f"used {item['tool']} "
                f"and produced "
                f"{item['result']}"
            )

        return " | ".join(context)


# ==========================================
# RESOLVE PREVIOUS RESULT
# ==========================================

def resolve_task(
    task,
    context
):

    if "{previous_result}" in task:

        previous = (
            context.latest_result()
        )

        if previous is None:
            previous = ""

        return task.replace(
            "{previous_result}",
            str(previous)
        )

    return task


# ==========================================
# TOOL EXECUTION
# ==========================================

def execute_tool(
    task,
    tool,
    context=None
):

    if tool == "calculator":

        expression = (
            task
            .lower()
            .replace(
                "calculate",
                "",
                1
            )
            .strip()
        )

        return calculator(
            expression
        )

    if tool == "expression_calculator":

        expression = (
            task
            .lower()
            .replace(
                "calculate",
                "",
                1
            )
            .strip()
        )

        return expression_calculator(
            expression
        )

    if tool == "word_counter":

        text = (
            task
            .lower()
            .replace(
                "count words",
                "",
                1
            )
            .strip()
        )

        return word_counter(
            text
        )

    if tool == "research_tool":

        query = task

        prefixes = [
            "research",
            "search",
            "look up",
            "find information about"
        ]

        for prefix in prefixes:

            if query.lower().startswith(prefix):

                query = query[
                    len(prefix):
                ].strip()

                break

        return research_tool(
            query
        )

    if tool == "coding_tool":

        return coding_tool(
            task
        )

    if tool == "file_tool":

        return file_tool(
            task
        )

    if tool == "data_tool":

        return data_tool(
            task
        )

    return "Error: No suitable tool."


# ==========================================
# PLAN BUILDER
# ==========================================

def build_plan(task):

    task_type = detect_task_type(
        task
    )

    # Multi-step always gets
    # the explicit local planner.
    if task_type == "multi_step":

        print(
            "\nTask Analyzer: "
            "MULTI-STEP TASK"
        )

        print(
            "Planning source: "
            "LOCAL MULTI-STEP PLANNER"
        )

        return plan_task(task)

    # Try learned strategy.
    strategy = select_strategy(
        task
    )

    if strategy:

        print(
            "\nPlanning source: "
            "LEARNED STRATEGY"
        )

        print(
            "Learning: Reusing "
            "learned strategy:",
            strategy
        )

        return [
            {
                "tool": strategy,
                "task": task
            }
        ]

    # Try LLM planner.
    print(
        "\nNo suitable learned strategy."
    )

    print(
        "Trying LLM Planner..."
    )

    llm_plan = get_llm_plan(
        task
    )

    if llm_plan:

        print(
            "Planning source: "
            "LLM PLANNER"
        )

        return llm_plan

    # Local fallback.
    print(
        "LLM unavailable."
    )

    print(
        "Using Local Planner..."
    )

    return plan_task(task)


# ==========================================
# RUN AGENT
# ==========================================

def run_agent(task):

    print(
        "\nAgent received:",
        task
    )

    print("=" * 40)

    plan = build_plan(task)

    print(
        "\n========== PLAN =========="
    )

    for i, step in enumerate(
        plan,
        start=1
    ):

        print(
            f"Step {i}: "
            f"{step['tool']} -> "
            f"{step['task']}"
        )

    print(
        "=========================="
    )

    context = AgentContext()

    step_results = []

    # ======================================
    # EXECUTE PLAN
    # ======================================

    for i, step in enumerate(
        plan,
        start=1
    ):

        original_task = (
            step["task"]
        )

        tool = step["tool"]

        current_task = resolve_task(
            original_task,
            context
        )

        print(
            f"\n----- Executing Step {i} -----"
        )

        print(
            "Tool:",
            tool
        )

        print(
            "Task:",
            current_task
        )

        if context.results:

            print(
                "Previous context:",
                context.latest_result()
            )

        result = execute_tool(
            current_task,
            tool,
            context
        )

        print(
            "Result:",
            result
        )

        success = evaluate_result(
            result
        )

        # ==================================
        # SUCCESS
        # ==================================

        if success:

            print(
                "Step evaluator: SUCCESS"
            )

            context.add_result(
                i,
                current_task,
                tool,
                result
            )

            save_memory(
                current_task,
                tool,
                result,
                True,
                False,
                context.get_context_text()
            )

            step_results.append({

                "step":
                    i,

                "tool":
                    tool,

                "task":
                    current_task,

                "result":
                    result,

                "success":
                    True,

                "retried":
                    False
            })

            continue

        # ==================================
        # FAILURE
        # ==================================

        print(
            "Step evaluator: FAILED"
        )

        alternative = (
            reflect_on_failure(
                current_task,
                tool,
                result
            )
        )

        retry_count = 0
        retry_success = False

        while (
            alternative
            and retry_count < MAX_RETRIES
        ):

            retry_count += 1

            print(
                f"\n----- RETRY "
                f"{retry_count} -----"
            )

            retry_result = execute_tool(
                current_task,
                alternative,
                context
            )

            print(
                "Retry result:",
                retry_result
            )

            retry_success = (
                evaluate_result(
                    retry_result
                )
            )

            if retry_success:

                print(
                    "Retry evaluator: "
                    "SUCCESS"
                )

                context.add_result(
                    i,
                    current_task,
                    alternative,
                    retry_result
                )

                save_memory(
                    current_task,
                    alternative,
                    retry_result,
                    True,
                    True,
                    context.get_context_text()
                )

                step_results.append({

                    "step":
                        i,

                    "tool":
                        alternative,

                    "task":
                        current_task,

                    "result":
                        retry_result,

                    "success":
                        True,

                    "retried":
                        True
                })

                break

            print(
                "Retry evaluator: FAILED"
            )

            save_memory(
                current_task,
                alternative,
                retry_result,
                False,
                True,
                context.get_context_text()
            )

            alternative = None

        if not retry_success:

            step_results.append({

                "step":
                    i,

                "tool":
                    tool,

                "task":
                    current_task,

                "result":
                    result,

                "success":
                    False,

                "retried":
                    retry_count > 0
            })

            print(
                "Plan stopped because "
                "the step failed."
            )

            break

    # ======================================
    # OVERALL EVALUATION
    # ======================================

    overall_success = evaluate_plan(
        step_results
    )

    print(
        "\n========== FINAL RESULT =========="
    )

    for step in step_results:

        print(
            f"Step {step['step']}: "
            f"{step['result']}"
        )

    print(
        "Overall success:",
        overall_success
    )

    print(
        "=================================="
    )

    return {

        "success":
            overall_success,

        "steps":
            step_results,

        "context":
            context.results
    }


# ==========================================
# INTERACTIVE MODE
# ==========================================

if __name__ == "__main__":

    print(
        "\nSELF-LEARNING AI AGENT"
    )

    print(
        "Type 'exit' to stop."
    )

    while True:

        task = input(
            "\nYou: "
        )

        if task.lower() in [
            "exit",
            "quit"
        ]:

            print(
                "Agent stopped."
            )

            break

        if not task.strip():
            continue

        run_agent(task)