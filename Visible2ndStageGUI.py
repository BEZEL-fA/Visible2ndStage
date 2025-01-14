import pygame
import time
from pygame.locals import *

# 初期化
pygame.init()
pygame.joystick.init()

# ウィンドウサイズ設定
WIDTH, HEIGHT = 400, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("R2 Trigger Sensitivity")

clock = pygame.time.Clock()

# ジョイスティックの設定
joystick_count = pygame.joystick.get_count()

if joystick_count == 0:
    print("No controller attached")
else:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        print(f"Controller {i}: {joystick.get_name()}")
    print("Select joystick number :")
    
    number = int(input())
    joystick = pygame.joystick.Joystick(number)
    joystick.init()
    print(f"Controller attached: {joystick.get_name()}")
    
axis_count = joystick.get_numaxes()
print(f"Number of axis: {axis_count}")

# Select axis signal
print("axis number :")
axis_number = int(input())

# メーターの初期設定
sens = 0
start_time = None
flag = 0  # Hold flag
BAR_WIDTH = 300
BAR_HEIGHT = 20
BAR_X = (WIDTH - BAR_WIDTH) // 2
BAR_Y = HEIGHT // 2

try:
    while True:
        # イベント処理
        for event in pygame.event.get():
            if event.type == JOYAXISMOTION and event.axis == axis_number:
                sens = (event.value + 1.0) / 2.0 * 255
                sens = int(sens)

        # 現在時刻
        current_time = time.time()

        # 判定ロジック
        if sens < 141:
            start_time = None
            flag = 0
        elif 141 <= sens < 220:
            if start_time is None:
                start_time = current_time
            flag = 1
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

        # 画面を黒でクリア
        screen.fill((0, 0, 0))

        # バーの色を決定
        if sens < 141:
            bar_color = (0, 255, 0)  # 緑
        elif 141 <= sens < 220:
            bar_color = (255, 255, 0)  # 黄色
        else:
            bar_color = (255, 0, 0)  # 赤

        # メーターの描画
        pygame.draw.rect(screen, (255, 255, 255), (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), 2)  # 外枠
        fill_width = int((sens / 255) * BAR_WIDTH)  # 圧力に応じた幅
        pygame.draw.rect(screen, bar_color, (BAR_X, BAR_Y, fill_width, BAR_HEIGHT))  # 内部バー

        # センシティビティ数値の表示
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Sensitivity: {sens}", True, (255, 255, 255))
        screen.blit(text, (BAR_X, BAR_Y - 40))

        # 画面更新
        pygame.display.update()
        pygame.time.wait(5)

# ctrl+c で終了
except KeyboardInterrupt:
    print("Exiting...")
    pygame.quit()
