import ast
import operator
import csv
import json
import os
import re
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


# ==========================================
# BASIC CALCULATOR
# ==========================================

def calculator(expression):
    return expression_calculator(expression)


# ==========================================
# SAFE EXPRESSION CALCULATOR
# ==========================================

def expression_calculator(expression):

    try:
        expression = (
            expression
            .strip()
            .replace("calculate", "", 1)
            .strip()
        )

        tree = ast.parse(
            expression,
            mode="eval"
        )

        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow
        }

        def calculate(node):

            if isinstance(node, ast.Constant):

                if isinstance(
                    node.value,
                    (int, float)
                ):
                    return node.value

                raise ValueError(
                    "Invalid number"
                )

            if isinstance(node, ast.UnaryOp):

                value = calculate(
                    node.operand
                )

                if isinstance(node.op, ast.USub):
                    return -value

                if isinstance(node.op, ast.UAdd):
                    return value

                raise ValueError(
                    "Unsupported unary operator"
                )

            if isinstance(node, ast.BinOp):

                left = calculate(node.left)
                right = calculate(node.right)

                operation = operators.get(
                    type(node.op)
                )

                if operation is None:
                    raise ValueError(
                        "Unsupported operator"
                    )

                return operation(
                    left,
                    right
                )

            raise ValueError(
                "Invalid expression"
            )

        return calculate(tree.body)

    except ZeroDivisionError:
        return "Error: Cannot divide by zero."

    except Exception as e:
        return f"Error: {e}"


# ==========================================
# WORD COUNTER
# ==========================================

def word_counter(text):
    return len(text.split())


# ==========================================
# RESEARCH TOOL
# ==========================================

def research_tool(query):

    query = query.strip()

    if not query:
        return "Error: Empty research query."

    try:

        search_url = (
            "https://en.wikipedia.org/w/api.php"
            "?action=query"
            "&list=search"
            "&format=json"
            "&utf8=1"
            "&srlimit=3"
            f"&srsearch={quote(query)}"
        )

        request = Request(
            search_url,
            headers={
                "User-Agent":
                    "SelfLearningAIAgent/1.0"
            }
        )

        with urlopen(
            request,
            timeout=8
        ) as response:

            data = json.loads(
                response.read().decode(
                    "utf-8"
                )
            )

        results = data.get(
            "query",
            {}
        ).get(
            "search",
            []
        )

        if not results:
            return (
                f"No research results found "
                f"for: {query}"
            )

        output = [
            f"Research results for: {query}"
        ]

        for index, item in enumerate(
            results,
            start=1
        ):

            title = item.get(
                "title",
                "Unknown"
            )

            snippet = re.sub(
                r"<.*?>",
                "",
                item.get(
                    "snippet",
                    ""
                )
            )

            output.append(
                f"{index}. {title}\n"
                f"   {snippet}"
            )

        return "\n".join(output)

    except Exception as e:

        return (
            "Research tool could not access "
            f"the research service: {e}"
        )


# ==========================================
# CODING TOOL
# ==========================================

def coding_tool(task):

    task = task.strip()

    if not task:
        return "Error: Empty coding task."

    # If the user provides Python code,
    # check whether it is syntactically valid.
    if (
        "def " in task
        or "import " in task
        or "class " in task
        or "print(" in task
    ):

        try:

            ast.parse(task)

            return (
                "Code analysis result:\n"
                "Python syntax is valid."
            )

        except SyntaxError as e:

            return (
                "Code analysis result:\n"
                f"Syntax error at line "
                f"{e.lineno}: {e.msg}"
            )

    # Built-in simple coding patterns.
    lower = task.lower()

    if (
        "reverse a string" in lower
        or "reverse string" in lower
    ):

        return (
            "Python solution:\n\n"
            "def reverse_string(text):\n"
            "    return text[::-1]"
        )

    if (
        "factorial" in lower
        and "function" in lower
    ):

        return (
            "Python solution:\n\n"
            "def factorial(n):\n"
            "    if n <= 1:\n"
            "        return 1\n"
            "    return n * factorial(n - 1)"
        )

    if (
        "fibonacci" in lower
        and "function" in lower
    ):

        return (
            "Python solution:\n\n"
            "def fibonacci(n):\n"
            "    a, b = 0, 1\n"
            "    for _ in range(n):\n"
            "        a, b = b, a + b\n"
            "    return a"
        )

    return (
        "Coding task received.\n"
        "No built-in solution matched this task. "
        "An LLM coding backend can be connected "
        "through the LLM planner."
    )


# ==========================================
# SAFE FILE TOOL
# ==========================================

def _project_directory():

    return Path(__file__).resolve().parent


def _safe_path(filename):

    filename = filename.strip()
    filename = filename.strip("\"'")

    path = Path(filename)

    if not path.is_absolute():
        path = _project_directory() / path

    path = path.resolve()

    root = _project_directory().resolve()

    try:
        path.relative_to(root)
    except ValueError:
        raise ValueError(
            "File must be inside the project directory."
        )

    return path


def file_tool(task):

    task = task.strip()

    if not task:
        return "Error: Empty file task."

    lower = task.lower()

    # READ
    if (
        lower.startswith("read ")
        or "read file" in lower
        or lower.startswith("open ")
    ):

        match = re.search(
            r"(?:read file|read|open)\s+(.+)",
            task,
            re.IGNORECASE
        )

        if not match:
            return "Error: Could not identify the file."

        filename = match.group(1).strip()

        try:

            path = _safe_path(filename)

            if not path.exists():
                return (
                    f"Error: File not found: "
                    f"{filename}"
                )

            if not path.is_file():
                return "Error: Path is not a file."

            content = path.read_text(
                encoding="utf-8",
                errors="replace"
            )

            if not content:
                return "File is empty."

            return (
                f"File: {path.name}\n"
                f"Characters: {len(content)}\n"
                f"Words: {len(content.split())}\n\n"
                f"{content[:5000]}"
            )

        except Exception as e:
            return f"File error: {e}"

    # LIST
    if (
        "list files" in lower
        or lower == "list files"
    ):

        try:

            files = [
                item.name
                for item in _project_directory().iterdir()
                if item.is_file()
            ]

            if not files:
                return "No files found."

            return (
                "Project files:\n"
                + "\n".join(
                    f"- {name}"
                    for name in sorted(files)
                )
            )

        except Exception as e:
            return f"File error: {e}"

    # SEARCH
    if "find " in lower or "search for " in lower:

        match = re.search(
            r"(?:find|search for)\s+(.+)",
            task,
            re.IGNORECASE
        )

        if not match:
            return "Error: Search text not found."

        search_text = (
            match.group(1)
            .strip()
            .strip("\"'")
        )

        matches = []

        for path in _project_directory().rglob("*"):

            if not path.is_file():
                continue

            if any(
                part.startswith(".")
                for part in path.parts
            ):
                continue

            try:

                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                if search_text.lower() in content.lower():

                    matches.append(
                        str(
                            path.relative_to(
                                _project_directory()
                            )
                        )
                    )

            except Exception:
                continue

        if not matches:
            return (
                f"No files contain: "
                f"{search_text}"
            )

        return (
            "Matching files:\n"
            + "\n".join(
                f"- {item}"
                for item in matches
            )
        )

    return (
        "File tool supports:\n"
        "- read <filename>\n"
        "- list files\n"
        "- find <text>"
    )


# ==========================================
# DATA TOOL
# ==========================================

def data_tool(task):

    task = task.strip()

    if not task:
        return "Error: Empty data task."

    match = re.search(
        r"(?:analyze|analyse|read|inspect)\s+(.+)",
        task,
        re.IGNORECASE
    )

    if match:
        filename = match.group(1).strip()
    else:
        filename = task

    try:

        path = _safe_path(filename)

        if not path.exists():
            return (
                f"Error: Data file not found: "
                f"{filename}"
            )

        suffix = path.suffix.lower()

        # CSV
        if suffix == ".csv":

            with open(
                path,
                "r",
                encoding="utf-8",
                errors="replace",
                newline=""
            ) as file:

                rows = list(
                    csv.DictReader(file)
                )

            if not rows:
                return "CSV file is empty."

            columns = list(
                rows[0].keys()
            )

            output = [
                f"Dataset: {path.name}",
                f"Rows: {len(rows)}",
                f"Columns: {len(columns)}",
                f"Column names: {columns}"
            ]

            for column in columns:

                numeric = []

                for row in rows:

                    try:
                        numeric.append(
                            float(
                                row[column]
                            )
                        )
                    except (
                        ValueError,
                        TypeError
                    ):
                        pass

                if numeric:

                    average = (
                        sum(numeric)
                        / len(numeric)
                    )

                    output.append(
                        f"{column}: "
                        f"numeric values={len(numeric)}, "
                        f"average={average:.2f}, "
                        f"min={min(numeric):.2f}, "
                        f"max={max(numeric):.2f}"
                    )

            return "\n".join(output)

        # JSON
        if suffix == ".json":

            with open(
                path,
                "r",
                encoding="utf-8",
                errors="replace"
            ) as file:

                data = json.load(file)

            if isinstance(data, list):

                return (
                    f"JSON dataset: {path.name}\n"
                    f"Records: {len(data)}\n"
                    f"Type: list"
                )

            if isinstance(data, dict):

                return (
                    f"JSON dataset: {path.name}\n"
                    f"Keys: {list(data.keys())}\n"
                    f"Type: object"
                )

            return (
                f"JSON dataset: {path.name}\n"
                f"Type: {type(data).__name__}"
            )

        return (
            "Unsupported data format. "
            "Use CSV or JSON."
        )

    except Exception as e:

        return f"Data error: {e}"


# ==========================================
# TOOL REGISTRY
# ==========================================

TOOLS = {

    "calculator":
        calculator,

    "expression_calculator":
        expression_calculator,

    "word_counter":
        word_counter,

    "research_tool":
        research_tool,

    "coding_tool":
        coding_tool,

    "file_tool":
        file_tool,

    "data_tool":
        data_tool
}