def evaluate_result(result):

    if result is None:
        return False

    if isinstance(
        result,
        str
    ):

        error_words = [
            "error",
            "failed",
            "cannot",
            "unknown",
            "invalid",
            "unsupported"
        ]

        for word in error_words:

            if word in result.lower():

                return False

    return True


def evaluate_plan(
    step_results
):

    if not step_results:

        return False

    for step in step_results:

        if not step.get(
            "success",
            False
        ):

            return False

    return True