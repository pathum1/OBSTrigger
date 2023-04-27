# **OBSTrigger**

Easily create and manage OBS Studio scenarios with the OBSTrigger. This Python-based application offers a simple and user-friendly interface to control your scenes, sources in OBS, triggered by Dota 2 in-game events (Kill, Death, or Assist).

## **Features**

🔷 **Create, Edit, and Delete Scenarios**: Easily set up and manage your OBS Studio scenarios.

🔷 **Automatic Scene and Source Switching**: Automatically switch scenes and sources in OBS Studio based on the selected Dota 2 in-game event.

🔷 **Intuitive GUI**: A simple graphical user interface built with Tkinter makes managing your scenarios a breeze.

🔷 **Save and Load Scenarios**: Save your scenarios to a file and load them in future sessions.

## **Installation**

**1. Clone the Repository**

```
git clone https://github.com/pathum1/OBSTrigger.git
```

**2. Change into the Cloned Directory**

```
cd OBSTrigger
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

**Use the intuitive interface to create, edit, and delete scenarios, and watch as OBS Studio automatically switches scenes and sources based on your settings.**

**🌟 Support the Project: If you find OBSTrigger useful, consider supporting the project through GitHub Sponsors or by clicking the donation button below:** - to be notified


