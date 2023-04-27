# **OBSTrigger**

OBSTrigger is a Python-based application that allows users to create and manage scenarios for OBS Studio. Each scenario consists of a scene, a source, and an event (Kill, Death, or Assist). The application communicates with OBS Studio through the OBS Websocket API to fetch and update scenes and sources.

## **Features**
🔷Create, edit, and delete scenarios.

🔷Automatically switch OBS scenes and sources based on the selected event.

🔷Easy-to-use graphical user interface (GUI) built using Tkinter.

🔷Saves scenarios to a file, allowing you to load them in future sessions.


## **Installation**

**1. Clone the repository**
```
git clone https://github.com/pathum1/OBSTrigger.git
```

**2. Change into the cloned directory**
```
cd obs-scenario-switcher
```

**3.(Optional) Create a virtual environment and activate it**
```
python -m venv venv
source venv/bin/activate  # For Linux and macOS
venv\Scripts\activate     # For Windows
```

**4. Install the required dependencies**
```
pip install -r requirements.txt
```


## **Usage**
**✔ Make sure OBS Studio is running with the OBS Websocket plugin installed and configured.**

**✔Run the OBSTrigger application:**

```
python main.py
```

**✔ Create, edit, and delete scenarios using the provided buttons and windows.**

**✔ application will automatically switch OBS scenes and sources based on the selected event in each scenario.**


## **Dependencies** 

**⚡Python 3.6 or higher**

**⚡Tkinter (built-in with Python)**

**⚡obs-websocket-py**

**⚡requests**
