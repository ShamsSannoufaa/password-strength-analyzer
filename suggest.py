import random
from typing import List

SPECIALS = "!@#$%^&*_-+=?"
WORDS = [
    "Tiger", "Ocean", "Falcon", "Shadow", "Matrix",
    "Rocket", "Storm", "Pixel", "Cobra", "Phoenix"
]

LEET_MAP = {
    "a": "@",
    "A": "@",
    "s": "$",
    "S": "$",
    "i": "1",
    "I": "1",
    "o": "0",
    "O": "0",
    "e": "3",
    "E": "3",
    "t": "7",
    "T": "7"
}


def has_upper(password: str) -> bool:
    return any(c.isupper() for c in password)


def has_lower(password: str) -> bool:
    return any(c.islower() for c in password)


def has_digit(password: str) -> bool:
    return any(c.isdigit() for c in password)


def has_special(password: str) -> bool:
    return any(not c.isalnum() for c in password)


def apply_leet(text: str, probability: float = 0.35) -> str:
    chars = []
    for ch in text:
        if ch in LEET_MAP and random.random() < probability:
            chars.append(LEET_MAP[ch])
        else:
            chars.append(ch)
    return "".join(chars)


def ensure_strength(base: str, min_len: int = 12) -> str:
    result = base

    if not has_upper(result):
        pos = random.randint(0, len(result))
        result = result[:pos] + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + result[pos:]

    if not has_lower(result):
        pos = random.randint(0, len(result))
        result = result[:pos] + random.choice("abcdefghijklmnopqrstuvwxyz") + result[pos:]

    if not has_digit(result):
        pos = random.randint(0, len(result))
        result = result[:pos] + random.choice("0123456789") + result[pos:]

    if not has_special(result):
        pos = random.randint(0, len(result))
        result = result[:pos] + random.choice(SPECIALS) + result[pos:]

    while len(result) < min_len:
        result += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" + SPECIALS)

    return result


def suggest_from_existing(password: str) -> str:
    base = password.strip()
    if not base:
        base = random.choice(WORDS)

    base = apply_leet(base)
    base = ensure_strength(base, min_len=12)
    return base


def suggest_restructured(password: str) -> str:
    core = password.strip()
    if not core:
        core = random.choice(WORDS)

    word = random.choice(WORDS)
    number = str(random.randint(100, 9999))
    special = random.choice(SPECIALS)

    candidates = [
        f"{word}{special}{core}{number}",
        f"{core}{special}{word}{number}",
        f"{word[:3]}{special}{core[::-1]}{number}",
        f"{core.capitalize()}{number}{special}{word[-3:]}"
    ]

    choice = random.choice(candidates)
    choice = apply_leet(choice, probability=0.2)
    choice = ensure_strength(choice, min_len=12)
    return choice


def generate_random_strong_password(length: int = 14) -> str:
    pools = {
        "upper": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "lower": "abcdefghijklmnopqrstuvwxyz",
        "digit": "0123456789",
        "special": SPECIALS
    }

    password_chars = [
        random.choice(pools["upper"]),
        random.choice(pools["lower"]),
        random.choice(pools["digit"]),
        random.choice(pools["special"]),
    ]

    all_chars = "".join(pools.values())
    while len(password_chars) < length:
        password_chars.append(random.choice(all_chars))

    random.shuffle(password_chars)
    return "".join(password_chars)


def generate_stronger_passwords(password: str, count: int = 3) -> List[str]:
    suggestions = [
        suggest_from_existing(password),
        suggest_restructured(password),
        generate_random_strong_password(length=random.randint(12, 16)),
    ]

    unique = []
    for s in suggestions:
        if s not in unique and s != password:
            unique.append(s)

    return unique[:count]