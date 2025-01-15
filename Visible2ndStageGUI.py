import os
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
import pygame
import time
from pygame.locals import *
import tkinter as tk
from tkinter import ttk
import sys
import math

# 初期化
pygame.init()
pygame.joystick.init()

# Tkinter ウィンドウの設定
root = tk.Tk()
iconfile = './images/icon1.ico'
root.iconbitmap(default=iconfile)
root.title("Select Joystick and Axis")

# ジョイスティックリスト取得
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    # ジョイスティックがない場合はエラーメッセージを表示
    error_label = ttk.Label(root, text="No joystick found", foreground="red", font=("Helvetica", 14))
    error_label.pack(pady=20)
    root.mainloop()  # Tkinter ウィンドウを表示して終了しないようにする
    pygame.quit()
    sys.exit()

joystick_options = [f"{i}: {pygame.joystick.Joystick(i).get_name()}" for i in range(joystick_count)]
selected_joystick = tk.StringVar(value=joystick_options[0])

def update_axis_dropdown(*args):
    """ジョイスティック選択に応じて軸の選択肢を更新する"""
    joystick_index = int(selected_joystick.get().split(":")[0])
    joystick = pygame.joystick.Joystick(joystick_index)
    joystick.init()
    axis_count = joystick.get_numaxes()
    axis_options = [f"Axis {i}" for i in range(axis_count)]
    axis_dropdown["values"] = axis_options
    selected_axis.set(axis_options[0])

# Tkinter ウィジェット
frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E))

# ジョイスティック選択メニュー
ttk.Label(frame, text="Select Joystick:").grid(column=0, row=0, sticky=tk.W)
joystick_dropdown = ttk.Combobox(frame, textvariable=selected_joystick, values=joystick_options, state="readonly")
joystick_dropdown.grid(column=1, row=0, sticky=(tk.W, tk.E))
joystick_dropdown.bind("<<ComboboxSelected>>", update_axis_dropdown)

# 軸選択メニュー
ttk.Label(frame, text="Select Axis:").grid(column=0, row=1, sticky=tk.W)
selected_axis = tk.StringVar()
axis_dropdown = ttk.Combobox(frame, textvariable=selected_axis, state="readonly")
axis_dropdown.grid(column=1, row=1, sticky=(tk.W, tk.E))

# 初期化時に軸選択肢を設定
update_axis_dropdown()

# 決定ボタン
def on_select():
    global joystick, axis_number
    joystick_index = int(selected_joystick.get().split(":")[0])
    joystick = pygame.joystick.Joystick(joystick_index)
    joystick.init()
    axis_number = int(selected_axis.get().split(" ")[1])
    root.destroy()

ttk.Button(frame, text="Start", command=on_select).grid(column=0, row=2, columnspan=2)

root.mainloop()

# 以下のコードはそのまま残す
# 円の扇形を塗りつぶす処理
def fill_segment_on_arc(start_angle, end_angle, color):
    # 扇形の頂点を計算
    points = [CIRCLE_CENTER]
    step = 1  # 精度を上げたい場合は小さくしてみてください（より多くの三角形を描画する）
    for angle in range(int(start_angle), int(end_angle), step):
        angle_rad = math.radians(angle)
        x = CIRCLE_CENTER[0] + CIRCLE_RADIUS * math.cos(angle_rad)
        y = CIRCLE_CENTER[1] - CIRCLE_RADIUS * math.sin(angle_rad)
        points.append((x, y))
    points.append(CIRCLE_CENTER)  # 終点を中心に戻す
    pygame.draw.polygon(screen, color, points)

# Pygame メイン処理
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame_icon = pygame.image.load('./images/icon1.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Visible2ndStage")

# メーターの初期設定
sens = 0
start_time = None
flag = 0
BAR_WIDTH = 300
BAR_HEIGHT = 20
BAR_X = (WIDTH - BAR_WIDTH) // 2
BAR_Y = HEIGHT // 2
CIRCLE_CENTER = (WIDTH // 2, HEIGHT - 60)
CIRCLE_RADIUS = 30
ARC_WIDTH = 5

try:
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # Xボタンがクリックされたときに終了
                pygame.quit()
                sys.exit()

            if event.type == JOYAXISMOTION and event.axis == axis_number:
                sens = (event.value + 1.0) / 2.0 * 255
                sens = int(sens)

        current_time = time.time()
        elapsed_time = 0
        if sens < 155:
            start_time = None
            flag = 0
        elif 155 <= sens < 220:
            if start_time is None:
                start_time = current_time
            flag = 1
            elapsed_time = current_time - start_time
        elif sens >= 220 and flag == 1:
            if start_time is not None:
                elapsed_time = current_time - start_time
                if 0.2 <= elapsed_time <= 0.366:
                    print("SS Successed")
                    print(f"{elapsed_time:.3f} seconds\n")
                else:
                    print("SS failed")
                    print(f"{elapsed_time:.3f} seconds\n")
                start_time = None
            flag = 0

        screen.fill((0, 0, 0))
        if sens < 155:
            bar_color = (0, 255, 0)
        elif 155 <= sens < 220:
            bar_color = (255, 255, 0)
        else:
            bar_color = (255, 0, 0)

        pygame.draw.rect(screen, (255, 255, 255), (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), 2)
        fill_width = int((sens / 255) * BAR_WIDTH)
        pygame.draw.rect(screen, bar_color, (BAR_X, BAR_Y, fill_width, BAR_HEIGHT))
        boundary_140_x = BAR_X + int((155 / 255) * BAR_WIDTH)
        boundary_220_x = BAR_X + int((220 / 255) * BAR_WIDTH)
        pygame.draw.line(screen, (255, 255, 255), (boundary_140_x, BAR_Y), (boundary_140_x, BAR_Y + BAR_HEIGHT), 2)
        pygame.draw.line(screen, (255, 255, 255), (boundary_220_x, BAR_Y), (boundary_220_x, BAR_Y + BAR_HEIGHT), 2)
        pygame.draw.circle(screen, (255, 255, 255), CIRCLE_CENTER, CIRCLE_RADIUS, 1)  # 円の縁に白い細い線を描画

        # t=0.2~0.366の間をグレーで塗りつぶす
        angle_0_2 = (0.2 / 0.366) * 360  # 0.2秒に対応する角度
        angle_0_366 = 360  # 0.366秒に対応する角度（最大360度）
        fill_segment_on_arc(angle_0_2, angle_0_366, (169, 169, 169))  # グレー色で塗りつぶし

        if start_time is not None:
            angle = min((elapsed_time / 0.366) * 360, 360)
            end_angle = angle * (3.14159 / 180)
            color = (255, 0, 0) if 0.2 <= elapsed_time <= 0.366 else (0, 255, 0)
            pygame.draw.arc(screen, color, 
                            (CIRCLE_CENTER[0] - CIRCLE_RADIUS, CIRCLE_CENTER[1] - CIRCLE_RADIUS, 
                             CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), 
                            0, end_angle, ARC_WIDTH)
        else:
            # Radを0にする
            angle = 0
            end_angle = angle * (3.14159 / 180)  # Angleをラジアンに

        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Sensitivity: {sens}", True, (255, 255, 255))
        screen.blit(text, (BAR_X, BAR_Y - 40))
        pygame.display.update()
        pygame.time.wait(5)

except KeyboardInterrupt:
    print("Exiting...")
    pygame.quit()