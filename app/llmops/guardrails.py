FORBIDDEN_PATTERNS = [
    "DROP TABLE",
    "ignore previous instructions",
]


def validate_prompt(prompt: str):
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.lower() in prompt.lower():
            raise ValueError("Unsafe prompt detected")