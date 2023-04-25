import tkinter as tk
from tkinter import ttk
from utils import save_scenarios


def edit_scenario_window(client, scenarios_listbox, scenarios, selected_index):
    window = tk.Toplevel()
    window.geometry("800x600")
    scene_label = tk.Label(window, text="Scene:")
    scene_label.pack()
    scene_var = tk.StringVar(window)
    scene_menu = ttk.OptionMenu(window, scene_var, scenarios[selected_index]['scene'],
                                *["Vertical Scene", "Stream End", "Scene", "Stream Start"])
    scene_menu.pack()
    source_label = tk.Label(window, text="Source:")
    source_label.pack()
    source_var = tk.StringVar(window)
    source_menu = ttk.OptionMenu(window, source_var, scenarios[selected_index]['source'])
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
    event_menu = ttk.OptionMenu(window, event_var, scenarios[selected_index]['event'],
                                *["Kill", "Death", "Assist"])
    event_menu.pack()

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    save_button = tk.Button(button_frame, text="Save Scenario",
                            command=lambda: on_save_scenario(scene_var, source_var, event_var,
                                                             scenarios_listbox,
                                                             scenarios,
                                                             selected_index,
                                                             window))
    save_button.pack(side=tk.LEFT, padx=5)

    cancel_button = tk.Button(button_frame, text="Cancel", command=window.destroy)
    cancel_button.pack(side=tk.LEFT, padx=5)

    window.grab_set()


def on_save_scenario(scene_var, source_var, event_var,
                     scenarios_listbox, scenarios,
                     selected_index, window):
    scene_name = scene_var.get()
    source_name = source_var.get()
    event_name = event_var.get()
    scenario = {
        'scene': scene_name,
        'source': source_name,
        'event': event_name,
    }
    scenarios[selected_index] = scenario
    save_scenarios(scenarios)
    scenario_text = f"Scenario {selected_index + 1} -> {scene_name} -> {source_name} -> {event_name}"
    scenarios_listbox.delete(selected_index)
    scenarios_listbox.insert(selected_index, scenario_text)
    max_width = max(scenarios_listbox.winfo_reqwidth(), 200)
    scenarios_listbox.config(width=max_width)
    window.destroy()
