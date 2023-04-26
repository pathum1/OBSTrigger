import sys
import os
import logging
from flask import Flask, request
app = Flask(__name__)

# sys.stdout = open(os.devnull, 'w')
# sys.stderr = open(os.devnull, 'w')

# Configure the logger
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# Define global variables to hold the client and process_data objects
client = None
process_data_func = None


@app.route('/', methods=['POST'])
def handle_post():
    data = request.get_json()
    logging.debug(f"Incoming dataaaa: {data}")  # Add a print statement here
    process_data_func(client, data)
    # Extract specific information from the incoming data
    if 'map' in data and 'game_state' in data['map']:
        game_state = data['map']['game_state']
        logging.debug(f'Game State: {game_state}')
    if 'player' in data:
        if 'kills' in data['player']:
            kills = data['player']['kills']
            logging.debug(f'Kills: {kills}')
        if 'deaths' in data['player']:
            deaths = data['player']['deaths']
            logging.debug(f'Deaths: {deaths}')
        if 'assists' in data['player']:
            assists = data['player']['assists']
            logging.debug(f'Assists: {assists}')
    # Pass the extracted information to the process_data function in main.py
    process_data_func(client, data)  # Call the process_data function with the client object and extracted data

    return 'OK'


def run(client_obj, process_data):
    global client
    global process_data_func
    client = client_obj
    process_data_func = process_data
    app.run(port=4000)