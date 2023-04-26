import json


def load_scenarios():
    try:
        with open("scenarios.json", "r") as f:
            scenarios = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        scenarios = []

    return scenarios


def save_scenarios(scenarios):
    with open("scenarios.json", "w") as f:
        json.dump(scenarios, f, indent=2)

