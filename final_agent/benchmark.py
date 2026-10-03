import csv
import os

from agent import run_agent
from learning import learning_report


TEST_TASKS = [
    "Calculate 25 + 75",
    "Calculate 20 * 5",
    "Calculate 10 % 3",
    "Calculate 100 / 4",
    "Count words artificial intelligence agents",
    "Calculate 10 % 3 and then count words learning agents improve",
    "Write a Python function to reverse a string",
    "List files",
    "Research machine learning",
    "Analyze benchmark_data.csv",
]


def create_test_csv():
    """Create a temporary CSV file for testing the data tool."""

    data = [
        ["name", "age", "score"],
        ["Alice", 20, 85],
        ["Bob", 21, 90],
        ["Charlie", 22, 95],
    ]

    with open(
        "benchmark_data.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)
        writer.writerows(data)


def remove_test_csv():
    """Remove the temporary benchmark CSV file."""

    if os.path.exists("benchmark_data.csv"):
        os.remove("benchmark_data.csv")


def run_test_pass(tasks, pass_name):
    """Run one complete benchmark pass."""

    print("\n" + "=" * 60)
    print(pass_name)
    print("=" * 60)

    successful = 0
    failed = 0

    for index, task in enumerate(tasks, start=1):

        print(f"\n{'=' * 10} TEST {index} {'=' * 10}")
        print(f"Task: {task}")

        result = run_agent(task)

        if result:
            successful += 1
        else:
            failed += 1

    success_rate = (
        successful / len(tasks) * 100
        if tasks
        else 0
    )

    print("\n" + "-" * 60)
    print(f"{pass_name} RESULT")
    print("-" * 60)

    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {success_rate:.2f}%")

    return successful, failed


def print_learning_report():
    """Display the current learning statistics."""

    report = learning_report()

    print("\n" + "=" * 60)
    print("LEARNING REPORT")
    print("=" * 60)

    total = report.get("total_experiences", 0)
    successful = report.get("successful", 0)
    failed = report.get("failed", 0)

    overall_rate = (
        successful / total * 100
        if total
        else 0
    )

    print(f"Total experiences: {total}")
    print(f"Successful experiences: {successful}")
    print(f"Failed experiences: {failed}")
    print(f"Overall success rate: {overall_rate:.2f}%")

    print("\nTool performance:")

    tools = report.get("tools", {})

    for tool, stats in tools.items():

        total_tool = stats.get("total", 0)
        successful_tool = stats.get("successful", 0)

        tool_rate = (
            successful_tool / total_tool * 100
            if total_tool
            else 0
        )

        print(
            f"  {tool}: "
            f"{tool_rate:.2f}% "
            f"({successful_tool}/{total_tool})"
        )


def run_benchmark():

    print("\n" + "=" * 60)
    print("SELF-LEARNING AI AGENT")
    print("FINAL V6 VALIDATION BENCHMARK")
    print("=" * 60)

    # Create temporary CSV for the data-tool test.
    create_test_csv()

    try:

        # =========================================================
        # FIRST PASS
        # =========================================================

        first_success, first_failed = run_test_pass(
            TEST_TASKS,
            "FIRST PASS — INITIAL EXECUTION"
        )

        # =========================================================
        # SECOND PASS
        # =========================================================
        #
        # The same tasks are run again.
        #
        # This demonstrates that the agent can use strategies
        # learned from previous executions.
        #
        # =========================================================

        second_success, second_failed = run_test_pass(
            TEST_TASKS,
            "SECOND PASS — LEARNING & STRATEGY REUSE"
        )

    finally:

        # Remove temporary CSV after testing.
        remove_test_csv()

    # =============================================================
    # FINAL VALIDATION REPORT
    # =============================================================

    total_tasks = len(TEST_TASKS)

    first_rate = (
        first_success / total_tasks * 100
        if total_tasks
        else 0
    )

    second_rate = (
        second_success / total_tasks * 100
        if total_tasks
        else 0
    )

    print("\n" + "=" * 60)
    print("FINAL V6 VALIDATION REPORT")
    print("=" * 60)

    print(f"Tasks per pass: {total_tasks}")

    print("\nFirst pass:")
    print(f"  Successful: {first_success}")
    print(f"  Failed: {first_failed}")
    print(f"  Success rate: {first_rate:.2f}%")

    print("\nSecond pass:")
    print(f"  Successful: {second_success}")
    print(f"  Failed: {second_failed}")
    print(f"  Success rate: {second_rate:.2f}%")

    print("\nLearning validation:")
    print("  First pass = initial execution")
    print("  Second pass = strategy reuse")

    if (
        first_success == total_tasks
        and second_success == total_tasks
    ):
        print("  Learning/reuse validation: PASSED")
    else:
        print("  Learning/reuse validation: CHECK REQUIRED")

    # =============================================================
    # LEARNING REPORT
    # =============================================================

    print_learning_report()

    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()