import json
import os


def save_scenarios(scenarios):
    with open('scenarios.json', 'w') as f:
        json.dump(scenarios, f)


def load_scenarios():
    try:
        with open('scenarios.json', 'r') as f:
            scenarios = json.load(f)
            return scenarios
    except Exception as e:
        print(f"An error occurred while loading scenarios: {e}")


# def load_scenarios():
  #  if not os.path.exists('scenarios.json'):
  #      print("scenarios.json file not found")
  #      return []
   # with open('scenarios.json', 'r') as f:
      #  scenarios = json.load(f)
    # print(f"Loaded scenarios: {scenarios}")
    # return scenarios
