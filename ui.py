import os
import sys
import configparser
import pygame
import tkinter as tk
from tkinter import ttk

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

def select_joystick_and_axis():
    """Tkinterによるジョイスティック、軸、閾値の選択"""
    def get_joystick_options():
        """現在接続されているジョイスティックのリストを取得"""
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            return []
        return [f"{i}: {pygame.joystick.Joystick(i).get_name()}" for i in range(joystick_count)]

    def update_axis_dropdown(*args):
        """選択されたジョイスティックに基づき軸のリストを更新"""
        joystick_options = get_joystick_options()
        if not joystick_options:
            axis_dropdown["values"] = []
            selected_axis.set("")
            return

        joystick_index = int(selected_joystick.get().split(":")[0])
        axis_count = pygame.joystick.Joystick(joystick_index).get_numaxes()
        axis_dropdown["values"] = [f"Axis {i}" for i in range(axis_count)]
        if axis_count > 0:
            selected_axis.set(axis_dropdown["values"][0])
        else:
            selected_axis.set("")

    def update_joystick_list():
        """ジョイスティックのリストを更新"""
        joystick_options = get_joystick_options()
        joystick_dropdown["values"] = joystick_options
        if joystick_options:
            selected_joystick.set(joystick_options[0])
            update_axis_dropdown()
        else:
            selected_joystick.set("")
            axis_dropdown["values"] = []
            selected_axis.set("")

    def load_threshold():
        """settings.ini から Threshold の値を読み込む"""
        config = configparser.ConfigParser()
        if os.path.exists("settings.ini"):
            config.read("settings.ini")
            try:
                return int(config.get("Settings", "Threshold", fallback="0"))
            except ValueError:
                return 0
        return 0

    def save_threshold(value):
        """Threshold の値を settings.ini に保存"""
        config = configparser.ConfigParser()
        config["Settings"] = {"Threshold": value}
        with open("settings.ini", "w") as configfile:
            config.write(configfile)

    # Tkinter ウィンドウの設定
    root = tk.Tk()
    root.title("Select Joystick and Axis")
    root.geometry("500x250")
    iconfile = './images/icon1.ico'
    root.iconbitmap(default=iconfile)

    selected_joystick = tk.StringVar()
    selected_axis = tk.StringVar()
    threshold_value = tk.IntVar(value=load_threshold())

    # フレーム設定
    frame = ttk.Frame(root, padding="10")
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E))

    # ジョイスティック選択
    ttk.Label(frame, text="Select Joystick:").grid(column=0, row=0, sticky=tk.W)
    joystick_dropdown = ttk.Combobox(frame, textvariable=selected_joystick, state="readonly", width=40)
    joystick_dropdown.grid(column=1, row=0, sticky=(tk.W, tk.E))
    joystick_dropdown.bind("<<ComboboxSelected>>", update_axis_dropdown)

    # 軸選択
    ttk.Label(frame, text="Select Axis:").grid(column=0, row=1, sticky=tk.W)
    axis_dropdown = ttk.Combobox(frame, textvariable=selected_axis, state="readonly", width=40)
    axis_dropdown.grid(column=1, row=1, sticky=(tk.W, tk.E))

    # Threshold 項目
    ttk.Label(frame, text="Threshold:").grid(column=0, row=2, sticky=tk.W)
    threshold_spinbox = ttk.Spinbox(
        frame,
        from_=0,
        to=255,
        textvariable=threshold_value,
        width=10,
        justify="center"
    )
    threshold_spinbox.grid(column=1, row=2, sticky=(tk.W, tk.E))

    # "Update" ボタン
    ttk.Button(frame, text="Update", command=update_joystick_list).grid(column=0, row=3, columnspan=2, pady=5)

    # "Start" ボタン
    def on_select():
        if not selected_joystick.get() or not selected_axis.get():
            tk.messagebox.showerror("Error", "Please select a joystick and an axis.")
            return
        save_threshold(threshold_value.get())  # Threshold 値を保存
        root.quit()
        root.destroy()

    ttk.Button(frame, text="Start", command=on_select).grid(column=0, row=4, columnspan=2)

    # 初期値の設定
    update_joystick_list()

    root.mainloop()

    if not selected_joystick.get() or not selected_axis.get():
        pygame.quit()
        sys.exit("No joystick or axis selected.")

    return (
        int(selected_joystick.get().split(":")[0]),
        int(selected_axis.get().split(" ")[1]),
        threshold_value.get(),
    )