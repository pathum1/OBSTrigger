import tkinter as tk
from tkinter import ttk
import time
from utils import save_scenarios
import sys
import os
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image
from edit_delete import edit_scenario_window
from styles import apply_styles

# sys.stdout = open(os.devnull, 'w')
# sys.stderr = open(os.devnull, 'w')

# apply_styles()


def on_button_click(client, listbox):
    source_name = listbox.get(listbox.curselection())
    response2 = client.get_scene_item_id('Scene', source_name)
    source_id = response2.scene_item_id
    print(f"SourceID:{source_id}")
    client.set_scene_item_enabled('Scene', source_id, True)
    time.sleep(3)
    client.set_scene_item_enabled('Scene', source_id, False)


def on_scene_select(client, scene_var, listbox):
    listbox.delete(0, tk.END)
    scene_name = scene_var.get()
    response4 = client.get_scene_item_list(scene_name)
    scene_items = response4.scene_items
    for item in scene_items:
        listbox.insert(tk.END, item['sourceName'])


def on_save_scenario(scene_collection_var, scene_var, source_var, event_var, scenarios_listbox, scenarios, window):
    scene_collection_name = scene_collection_var.get()
    scene_name = scene_var.get()
    source_name = source_var.get()
    event_name = event_var.get()
    scenario = {
        'scene_collection': scene_collection_name,
        'scene': scene_name,
        'source': source_name,
        'event': event_name,
    }
    scenarios.append(scenario)
    save_scenarios(scenarios)
    scenario_text = f"Scenario {len(scenarios)} ▶ {scene_collection_name} ▶ {scene_name} ▶ {source_name} ▶ {event_name}"
    scenarios_listbox.insert(tk.END, scenario_text)
    window.destroy()


def test_scenario(client, scenario):
    response = client.get_scene_item_id(scenario['scene'], scenario['source'])
    scene_item_id = response.scene_item_id
    client.set_scene_item_enabled(scenario['scene'], scene_item_id, True)
    time.sleep(3)
    client.set_scene_item_enabled(scenario['scene'], scene_item_id, False)


# Add the update_visibility_label function here, above the create_scenario_window function
def update_visibility_label(client, scene_var, source_var, visibility_label):
    scene_name = scene_var.get()
    source_name = source_var.get()
    if scene_name and source_name:
        response = client.get_source_active(source_name)
        video_active = response.video_active
        video_showing = response.video_showing
        print(f"Source '{source_name}' active: {video_active}, showing: {video_showing}")
        if video_showing:
            visibility_label.config(text="❌")
        else:
            visibility_label.config(text="✔")
    else:
        print("No source selected")


def create_scenario_window(client, scenarios_listbox, scenarios):
    window = tk.Toplevel()
    window.geometry("800x600")

    # Create a function to fetch scene collections
    def fetch_scene_collections():
        def fetch_and_update():
            response = client.get_scene_collection_list()
            collections = [collection for collection in response.scene_collections]
            window.after(0, lambda: scene_collection_combobox.configure(values=collections))

        fetch_thread = threading.Thread(target=fetch_and_update)
        fetch_thread.start()

    # Create a dropdown for scene collections
    scene_collection_label = tk.Label(window, text="Scene Collection:")
    scene_collection_label.pack()
    scene_collection_var = tk.StringVar(window)
    scene_collection_combobox = ttk.Combobox(window, textvariable=scene_collection_var)
    scene_collection_combobox.pack()

    scene_label = tk.Label(window, text="Scene:")
    scene_label.pack()
    scene_var = tk.StringVar(window)
    scene_combobox = ttk.Combobox(window, textvariable=scene_var)
    scene_combobox.pack()

    def fetch_scenes():
        scene_combobox.set('')  # Clear the current value of the ComboBox
        response = client.get_scene_list()
        scenes = [scene['sceneName'] for scene in response.scenes]
        scene_combobox.configure(values=scenes)

    def fetch_initial_data():
        # Fetch the initial scene collections and scenes
        response1 = client.get_scene_collection_list()
        scene_collections = [collection for collection in response1.scene_collections]
        scene_collection_combobox.configure(values=scene_collections)

        # Fetch the initial scenes
        fetch_scenes()

    fetch_initial_data()

    source_label = tk.Label(window, text="Source:")
    source_label.pack()
    source_var = tk.StringVar(window)

    source_frame = tk.Frame(window)
    source_frame.pack()

    source_combobox = ttk.Combobox(source_frame, textvariable=source_var)
    source_combobox.pack(side=tk.LEFT)

    visibility_label = ttk.Label(source_frame, text=" ", style='Visibility.TLabel')
    visibility_label.pack(side=tk.RIGHT, padx=(5, 5))

    # source_label_frame = tk.Frame(window)  # New frame for the visibility label
    # source_label_frame.pack()  # Add this line to pack the new frame
    # Change it to this line
    source_combobox.bind('<<ComboboxSelected>>', lambda event: update_visibility_label(client, scene_var, source_var,
                                                                                        visibility_label))


    def fetch_sources():
        selected_scene = scene_var.get()
        if selected_scene:
            response = client.get_scene_item_list(selected_scene)
            sources = [item['sourceName'] for item in response.scene_items]
            source_combobox.configure(values=sources)
            source_combobox.set('')  # Clear the current value of the ComboBox

    scene_combobox.bind('<<ComboboxSelected>>', lambda event: fetch_sources())

    # Call the fetch_initial_data function to populate the Comboboxes
    fetch_initial_data()

    def on_source_select(source):
        source_var.set(source)

    def set_current_scene_collection(event=None):
        scene_collection_name = scene_collection_var.get()
        if scene_collection_name:
            client.set_current_scene_collection(scene_collection_name)
            # Update the scenes list when the scene collection changes
            fetch_scenes()

    scene_collection_combobox.bind('<<ComboboxSelected>>', set_current_scene_collection)

    event_label = tk.Label(window, text="Event:")
    event_label.pack()
    event_var = tk.StringVar(window)
    event_menu = ttk.OptionMenu(window, event_var, "Select an Event",
                                *["Kill", "Death", "Assist"])
    event_menu.pack()

    def test_selected_scenario():
        selected_index = scenarios_listbox.curselection()
        if selected_index:
            selected_scenario = scenarios[selected_index[0]]
            test_scenario(client, selected_scenario)

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    save_button = tk.Button(button_frame, text="Save Scenario",
                            command=lambda: on_save_scenario(scene_collection_var, scene_var, source_var, event_var,
                                                             scenarios_listbox,
                                                             scenarios, window))

    save_button.pack(side=tk.LEFT, padx=5)

    cancel_button = tk.Button(button_frame, text="Cancel", command=window.destroy)
    cancel_button.pack(side=tk.LEFT, padx=5)

    def update_save_button_state():
        if scene_var.get() != "Select a Scene" and source_var.get() != "Select a Source" and event_var.get() != \
                "Select an Event":
            save_button['state'] = tk.NORMAL
        else:
            save_button['state'] = tk.DISABLED

    scene_var.trace('w', lambda *args: update_save_button_state())
    source_var.trace('w', lambda *args: update_save_button_state())
    event_var.trace('w', lambda *args: update_save_button_state())

    save_button['state'] = tk.DISABLED

    window.grab_set()


def create_gui(client, scenarios):
    print("Creating GUI...")
    root = tk.Tk()
    root.geometry("800x600")
    print("Root window created")
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    scenarios_listbox = tk.Listbox(root, width=80, selectborderwidth=2, relief=tk.SUNKEN)
    scenarios_listbox.pack()
    edit_scenario_button = tk.Button(root, text="Edit Scenario")
    edit_scenario_button.pack(padx=100, pady=100)
    scrollbar = tk.Scrollbar(root, orient="vertical")
    scrollbar.config(command=scenarios_listbox.yview)
    scrollbar.pack(side="right", fill="y")

    def on_edit_scenario():
        selected_index = scenarios_listbox.curselection()[0]
        edit_scenario_window(client, scenarios_listbox, scenarios, selected_index)

    edit_scenario_button.config(command=on_edit_scenario)

    delete_scenario_button = tk.Button(button_frame, text="Delete Scenario")
    delete_scenario_button.pack(side=tk.LEFT, padx=5)

    def on_delete_scenario():
        selected_index = scenarios_listbox.curselection()[0]
        del scenarios[selected_index]
        save_scenarios(scenarios)
        scenarios_listbox.delete(selected_index)

    delete_scenario_button.config(command=on_delete_scenario)

    test_scenario_button = tk.Button(button_frame, text="Test Scenario", state=tk.DISABLED)
    test_scenario_button.pack(side=tk.LEFT, padx=5)

    def on_select_scenario(event):
        if scenarios_listbox.curselection():
            edit_scenario_button.config(state=tk.NORMAL)
            delete_scenario_button.config(state=tk.NORMAL)
            test_scenario_button.config(state=tk.NORMAL)  # Enable the Test Scenario button
        else:
            edit_scenario_button.config(state=tk.DISABLED)
            delete_scenario_button.config(state=tk.DISABLED)
            test_scenario_button.config(state=tk.DISABLED)  # Disable the Test Scenario button

    def on_test_scenario():
        selected_index = scenarios_listbox.curselection()[0]
        scenario = scenarios[selected_index]
        test_scenario(client, scenario)

    test_scenario_button.config(command=on_test_scenario)  # Move this line here

    scenarios_listbox.bind('<<ListboxSelect>>', on_select_scenario)
    edit_scenario_button.config(state=tk.DISABLED)
    delete_scenario_button.config(state=tk.DISABLED)

    scenarios_listbox.config(yscrollcommand=scrollbar.set)
    edit_scenario_button.config(state=tk.DISABLED)

    for i, scenario in enumerate(scenarios):
        scene_collection_text = scenario.get('scene_collection', 'Unknown')
        scenario_text = f"Scenario {i + 1} ▶ {scene_collection_text} ▶ {scenario['scene']} ▶ {scenario['source']} ▶ {scenario['event']}"
        scenarios_listbox.insert(tk.END, scenario_text)

    # max_width = max(scenarios_listbox.winfo_reqwidth(), 50)
    # scenarios_listbox.config(width=max_width)
    add_scenario_button = tk.Button(button_frame, text="Add Scenario", command=lambda: create_scenario_window(client,
                                                                                                              scenarios_listbox,
                                                                                                              scenarios))
    add_scenario_button.pack(side=tk.LEFT, padx=5)
    # edit_scenario_button = tk.Button(button_frame, text="Edit Scenario")
    # edit_scenario_button.pack(side=tk.LEFT, padx=5)

    def on_close():
        root.withdraw()
        icon.visible = True

    close_button = tk.Button(root, text="Close", command=on_close)
    close_button.pack()

    def on_restore():
        root.deiconify()
        icon.visible = False

    def on_exit():
        icon.stop()
        root.destroy()

    icon = Icon('My App', Image.open('icon.png'), menu=Menu(
        MenuItem('Restore', on_restore),
        MenuItem('Exit', on_exit)
    ))

    threading.Thread(target=icon.run).start()
    root.protocol('WM_DELETE_WINDOW', on_close)

    root.mainloop()
    print("GUI created")

