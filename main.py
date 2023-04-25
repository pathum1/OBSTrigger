import toml
import obsws_python as obs
from gui import create_gui
from dota2_gsi import run  # Import the run function from dota2_gsi.py
import threading
import time  # Import the time module
from utils import save_scenarios, load_scenarios
import logging
import sys
import os
from pystray import Icon, Menu, MenuItem
from PIL import Image

# sys.stdout = open(os.devnull, 'w')
# sys.stderr = open(os.devnull, 'w')

# Configure the logger
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Log a message
logging.warning('This is a warning message')

# Define a global variable to hold the previous game state
previous_game_state = {}


# Define a global variable to hold the list of scenarios
scenarios = []
scenarios = load_scenarios()

# Load the configuration file
config = toml.load('config.toml')

# Get the connection details from the config file
host = config['connection']['host']
port = config['connection']['port']
password = config['connection']['password']

client = obs.ReqClient(host=host, port=port, password=password)

# Load the list of scenarios from a file


def process_data(client, data):
    logging.debug(f"Data received by process_data: {data}")
    global previous_game_state  # Use the global previous_game_state variable

    # print("Processing data...")  # Add a print statement here
    # print(f"1 - Incoming data: {data}")  # Add a print statement here
    # Iterate over the list of scenarios
    for scenario in scenarios:
        logging.debug(f"Checking scenario: {scenario}")
        logging.debug(f"Scenario event: {scenario['event']}")
        logging.debug(f"'kills' in data: {'kills' in data}")
        # Check if the incoming data matches the scenario
        if scenario['event'] == 'Kill' and 'player' in data and 'kills' in data['player']:
            # Check if the kill count has increased
            if 'kills' not in previous_game_state or data['player']['kills'] > previous_game_state['kills']:
                logging.debug("Kill count has increased")

                # Get the sceneItemId for the selected source
                response = client.get_scene_item_id(scenario['scene'], scenario['source'])
                logging.debug(f"Response: {response}")
                scene_item_id = response.scene_item_id
                logging.debug(f"Scene Item ID: {scene_item_id}")
                # Enable the corresponding source in OBS using its sceneItemId
                client.set_scene_item_enabled(scenario['scene'], scene_item_id, True)
                logging.debug(f"Enabled source: {scenario['source']}")

                # Wait for 4 seconds
                time.sleep(4)

                # Disable the corresponding source in OBS using its sceneItemId
                client.set_scene_item_enabled(scenario['scene'], scene_item_id, False)
                logging.debug(f"Disabled source: {scenario['source']}")

        elif scenario['event'] == 'Death' and 'player' in data and 'deaths' in data['player']:
            # Check if the death count has increased
            if 'deaths' not in previous_game_state or data['player']['deaths'] > previous_game_state['deaths']:
                logging.debug("Death count has increased")

                # Get the sceneItemId for the selected source
                response = client.get_scene_item_id(scenario['scene'], scenario['source'])
                scene_item_id = response.scene_item_id

                # Enable the corresponding source in OBS using its sceneItemId
                client.set_scene_item_enabled(scenario['scene'], scene_item_id, True)
                logging.debug(f"Enabled source: {scenario['source']}")  # Add a print statement here

                # Wait for 4 seconds
                time.sleep(4)

                # Disable the corresponding source in OBS using its sceneItemId
                client.set_scene_item_enabled(scenario['scene'], scene_item_id, False)
                logging.debug(f"Disabled source: {scenario['source']}")  # Add a print statement here

        elif scenario['event'] == 'Assist' and 'player' in data and 'assists' in data['player']:
            # Check if the assist count has increased
            if 'assists' not in previous_game_state or data['player']['assists'] > previous_game_state['assists']:
                logging.debug("Assist count has increased")  # Add a print statement here

                # Get the sceneItemId for the selected source
                response = client.get_scene_item_id(scenario['scene'], scenario['source'])
                scene_item_id = response.scene_item_id

                # Enable the corresponding source in OBS using its sceneItemId
                client.set_scene_item_enabled(scenario['scene'], scene_item_id, True)
                logging.debug(f"Enabled source: {scenario['source']}")  # Add a print statement here

                # Wait for 4 seconds
                time.sleep(4)

                # Disable the corresponding source in OBS using its sceneItemId
                client.set_scene_item_enabled(scenario['scene'], scene_item_id, False)
                logging.debug(f"Disabled source: {scenario['source']}")  # Add a print statement here

    # Update the previous game state with the current game state
    if 'player' in data:
        if 'kills' in data['player']:
            previous_game_state['kills'] = data['player']['kills']
            logging.debug(f"Previous game state updated: {previous_game_state}")
        if 'deaths' in data['player']:
            previous_game_state['deaths'] = data['player']['deaths']
        if 'assists' in data['player']:
            previous_game_state['assists'] = data['player']['assists']


def on_close(window):
    # Hide the window
    window.withdraw()
    # Show the system tray icon
    icon.visible = True


def on_restore(window):
    # Show the window
    window.deiconify()
    # Hide the system tray icon
    icon.visible = False


def on_exit(icon, window):
    # Stop the system tray icon
    icon.stop()
    # Destroy the window
    window.destroy()


# Create a system tray icon with a menu
icon = Icon('My App', Image.open('icon.png'), menu=Menu(
    MenuItem('Restore', lambda: on_restore(window)),
    MenuItem('Exit', lambda: on_exit(icon, window))
))

# Start the Flask app in dota2_gsi.py and pass in the client object and process_data function
threading.Thread(target=run, args=(client, process_data)).start()  # Start the Flask app in a separate thread


# whether the source is active
# response1 = client.get_source_active('KILL_ALERT')
# print(f"KILLER_ALERT ACTIVE?: {response1.video_showing}")

# gets the list of scenes
response3 = client.get_scene_list()

# prints an array of scenes
# print(f"Scene list: {response3.scenes}")

create_gui(client, scenarios)
