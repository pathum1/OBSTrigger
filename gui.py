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


# sys.stdout = open(os.devnull, 'w')
# sys.stderr = open(os.devnull, 'w')


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


def on_save_scenario(scene_var, source_var, event_var, scenarios_listbox, scenarios, window):
    scene_name = scene_var.get()
    source_name = source_var.get()
    event_name = event_var.get()
    scenario = {
        'scene': scene_name,
        'source': source_name,
        'event': event_name,
    }
    scenarios.append(scenario)
    save_scenarios(scenarios)
    scenario_text = f"Scenario {len(scenarios)} -> {scene_name} -> {source_name} -> {event_name}"
    scenarios_listbox.insert(tk.END, scenario_text)
    max_width = max(scenarios_listbox.winfo_reqwidth(), 200)
    scenarios_listbox.config(width=max_width)
    window.destroy()


def test_scenario(client, scenario):
    response = client.get_scene_item_id(scenario['scene'], scenario['source'])
    scene_item_id = response.scene_item_id
    client.set_scene_item_enabled(scenario['scene'], scene_item_id, True)


def create_scenario_window(client, scenarios_listbox, scenarios):
    window = tk.Toplevel()
    window.geometry("800x600")
    scene_label = tk.Label(window, text="Scene:")
    scene_label.pack()
    scene_var = tk.StringVar(window)
    scene_menu = ttk.OptionMenu(window, scene_var, "Select a Scene",
                                *["Vertical Scene", "Stream End", "Scene", "Stream Start"])
    scene_menu.pack()
    source_label = tk.Label(window, text="Source:")
    source_label.pack()
    source_var = tk.StringVar(window)
    source_menu = ttk.OptionMenu(window, source_var, "Select a Source")
    source_menu.pack()

    def on_source_select(source):
        source_var.set(source)

    def on_scene_select_optionmenu(scene_name):
        response = client.get_scene_item_list(scene_name)
        sources = [item['sourceName'] for item in response.scene_items]
        source_menu['menu'].delete(0, 'end')
        for source in sources:
            source_menu['menu'].add_command(label=source,
                                            command=lambda src=source: on_source_select(src))

    scene_var.trace('w', lambda *args: on_scene_select_optionmenu(scene_var.get()))

    event_label = tk.Label(window, text="Event:")
    event_label.pack()
    event_var = tk.StringVar(window)
    event_menu = ttk.OptionMenu(window, event_var, "Select an Event",
                                *["Kill", "Death", "Assist"])
    event_menu.pack()

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    save_button = tk.Button(button_frame, text="Save Scenario",
                            command=lambda: on_save_scenario(scene_var, source_var, event_var, scenarios_listbox,
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

    scenarios_listbox = tk.Listbox(root)
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

    def on_select_scenario(event):
        if scenarios_listbox.curselection():
            edit_scenario_button.config(state=tk.NORMAL)
            delete_scenario_button.config(state=tk.NORMAL)
        else:
            edit_scenario_button.config(state=tk.DISABLED)
            delete_scenario_button.config(state=tk.DISABLED)

    scenarios_listbox.bind('<<ListboxSelect>>', on_select_scenario)
    edit_scenario_button.config(state=tk.DISABLED)
    delete_scenario_button.config(state=tk.DISABLED)

    scenarios_listbox.config(yscrollcommand=scrollbar.set)
    edit_scenario_button.config(state=tk.DISABLED)

    for i, scenario in enumerate(scenarios):
        scenario_text = f"Scenario {i + 1} -> {scenario['scene']} -> {scenario['source']} -> {scenario['event']}"
        scenarios_listbox.insert(tk.END, scenario_text)

    max_width = max(scenarios_listbox.winfo_reqwidth(), 50)
    scenarios_listbox.config(width=max_width)

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
