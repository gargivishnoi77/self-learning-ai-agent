import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


ALLOWED_TOOLS = {
    "calculator",
    "expression_calculator",
    "word_counter"
}


def get_llm_plan(task):

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:

        print(
            "LLM Planner: "
            "No API key available."
        )

        return None

    try:

        client = OpenAI(
            api_key=api_key
        )

        prompt = f"""
You are the planning module of a
self-learning AI agent.

User task:
{task}

Available tools:

calculator:
addition, subtraction,
multiplication, division.

expression_calculator:
mathematical expressions,
modulo, powers and complex arithmetic.

word_counter:
counts words in text.

Create the smallest correct execution plan.

For mathematical tasks, put the exact
mathematical expression in the task field.

For word counting, put only the text
that should be counted in the task field.

Return ONLY JSON:

{{
  "steps": [
    {{
      "tool": "tool_name",
      "task": "exact tool input"
    }}
  ]
}}
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        raw = (
            response.output_text
            .strip()
        )

        data = json.loads(
            raw
        )

        steps = data.get(
            "steps",
            []
        )

        validated = []

        for step in steps:

            if not isinstance(
                step,
                dict
            ):
                continue

            tool = step.get(
                "tool"
            )

            step_task = step.get(
                "task"
            )

            if (
                tool in ALLOWED_TOOLS
                and step_task
            ):

                validated.append(
                    {
                        "tool": tool,
                        "task": str(
                            step_task
                        )
                    }
                )

        if not validated:

            print(
                "LLM Planner: "
                "Invalid plan."
            )

            return None

        print(
            "LLM Planner: "
            "Plan generated successfully."
        )

        return validated

    except Exception as e:

        print(
            "LLM Planner unavailable:",
            e
        )

        return None