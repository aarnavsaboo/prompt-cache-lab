def conversation_prompts(turns: int, base_chars: int = 2000) -> list[str]:
    if turns < 1:
        return []
    base = (
        "Reference material for a repeated local language-model conversation. "
        "The same material remains available while new turns are appended. "
    )
    reference = (base * (base_chars // len(base) + 1))[:base_chars]
    messages = [reference]
    prompts = []
    for i in range(turns):
        messages.append(f"User turn {i}: provide a concise observation about local inference experiment {i}.")
        messages.append(f"Assistant turn {i}: previous response placeholder {i}.")
        prompts.append("\n".join(messages))
    return prompts
