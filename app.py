# Wahala Bot - Step 3: Mood Reader + Memory (memory.json) + safety check

import json
import os
import random

MEMORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory.json")

DANGER_WORDS = [
    "kill myself",
    "end my life",
    "end it all",
    "suicide",
    "wan die",
    "want to die",
    "no wan live",
    "take my own life",
]


def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    data.setdefault("name", None)
    data.setdefault("facts", [])
    return data


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


def greet(memory):
    name = memory["name"]
    facts = memory["facts"]

    if name and facts:
        return f"How far, {name}! Last time you tell me: \"{facts[-1]}\". How e dey go now?"
    if name:
        return f"How far, {name}! I don dey wait you. Wetin dey happen?"

    greetings = [
        "How far! Wahala Bot dey here. Wetin dey happen?",
        "Heyyy, how far? I dey o. Talk to me, abeg.",
        "Oya come, I don dey wait you. How body?",
    ]
    return random.choice(greetings)


def read_mood(user_text):
    text = user_text.strip()

    has_emoji = any(ord(ch) > 10000 for ch in text)
    has_excitement = "!!" in text
    letters = [ch for ch in text if ch.isalpha()]
    is_shouting = len(letters) >= 4 and all(ch.isupper() for ch in letters)

    if has_emoji or has_excitement or is_shouting:
        return "hyped"

    if len(text.split()) <= 3:
        return "soft"

    return "normal"


def reply(user_text, memory):
    text = user_text.lower().strip()
    original = user_text.strip()

    # 1. Safety check comes first, always
    for word in DANGER_WORDS:
        if word in text:
            return (
                "Hey, pause. I no wan joke now. Are you thinking of ending your life? "
                "Abeg tell me true, I no go judge you. If you dey in danger tonight, "
                "please call or go meet one person near you right now. I dey here with you."
            )

    # 2. Memory commands
    if text.startswith("my name is "):
        rest = original[len("my name is "):].strip()
        if rest:
            memory["name"] = rest.split()[0].title()
            save_memory(memory)
            return f"Nice to meet you, {memory['name']}! I don save am. I no go forget."

    if text.startswith("remember"):
        fact = original[len("remember"):].strip()
        if fact.lower().startswith("that "):
            fact = fact[5:].strip()
        if fact:
            memory["facts"].append(fact)
            save_memory(memory)
            return "Okay, I don save am. I go remember."
        return "Remember wetin? Tell me after the word 'remember'."

    if "what do you remember" in text or text == "memory":
        if not memory["name"] and not memory["facts"]:
            return "I never remember anything yet. Tell me say 'my name is ...' or 'remember that ...'."
        lines = []
        if memory["name"]:
            lines.append(f"Your name na {memory['name']}.")
        for fact in memory["facts"]:
            lines.append(f"- {fact}")
        return "Na this one I remember:\n" + "\n".join(lines)

    # 3. Mood replies
    mood = read_mood(user_text)

    if mood == "hyped":
        return "EHEN!! See energy! 😂🔥 Abeg wetin dey sup, I dey vibe with you!!"

    if mood == "soft" and ("fine" in text or "ok" in text):
        return "Hmm... you sure say you dey fine? Abeg talk true to me, small small. I dey here."

    # 4. Normal replies
    if "how far" in text or text in ("hi", "hello", "hey"):
        return "I dey o! No wahala. You self, how you dey?"

    if "fine" in text or "good" in text:
        return "Ahh, that one sweet me. No wahala at all."

    if "tired" in text or "stress" in text:
        return "Ah ah, abeg rest small. Body no be firewood."

    if "school" in text or "babcock" in text or "exam" in text or "assignment" in text:
        return "Eeh, school wahala! 😩 Which one be the main problem: lecturer, money, or the work?"

    if "bye" in text or "exit" in text:
        return "Alright o, I go see you later. Take care of yourself! 👋"

    fallbacks = [
        "Hmm, I hear you. Tell me more, abeg.",
        "Ehn? See me, I dey listen. Wetin happen next?",
        "Ah ah, na so? Continue, I dey here.",
        "No wahala, talk am. I no go judge.",
    ]
    return random.choice(fallbacks)


def main():
    memory = load_memory()

    print("=" * 40)
    print("   WAHALA BOT")
    print("   (type 'bye' to exit)")
    print("=" * 40)
    print()
    print("Wahala Bot:", greet(memory))

    while True:
        user_text = input("\nYou: ")
        response = reply(user_text, memory)
        print("Wahala Bot:", response)

        if "bye" in user_text.lower() or "exit" in user_text.lower():
            break


if __name__ == "__main__":
    main()