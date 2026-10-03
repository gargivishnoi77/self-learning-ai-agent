from memory import (
    get_relevant_memory
)


def reflect_on_failure(
    task,
    failed_tool,
    failed_result
):

    print(
        "\n========== REFLECTION =========="
    )

    print(
        "Previous attempt failed."
    )

    print(
        "Failed tool:",
        failed_tool
    )

    print(
        "Failed result:",
        failed_result
    )

    memory = get_relevant_memory(
        task
    )

    for experience in reversed(
        memory
    ):

        if (
            experience.get(
                "success",
                False
            )
            and
            experience.get(
                "tool"
            ) != failed_tool
        ):

            alternative = (
                experience["tool"]
            )

            print(
                "Reflection: "
                "Alternative strategy =",
                alternative
            )

            print(
                "================================"
            )

            return alternative

    print(
        "Reflection: "
        "No alternative strategy found."
    )

    print(
        "================================"
    )

    return None