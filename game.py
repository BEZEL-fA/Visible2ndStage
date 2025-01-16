import sys
import pygame
import time
import math
from ui import select_joystick_and_axis
import ctypes
import win32gui, win32con, win32api

# 定数の定義
WIDTH, HEIGHT = 400, 300
BAR_WIDTH, BAR_HEIGHT = 300, 20
CIRCLE_RADIUS = 30
CIRCLE_CENTER = (WIDTH // 2, HEIGHT - 90)
TIME1 = 0.2
TIME2 = 0.366
ARC_WIDTH = 5
screen_width, screen_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
window_width, window_height = WIDTH, HEIGHT
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

def fill_segment_on_arc(screen, center, radius, start_angle, end_angle, color):
    """円の扇形を塗りつぶす"""
    points = [center]
    step = 1  # 精度
    for angle in range(int(start_angle), int(end_angle), step):
        angle_rad = math.radians(angle)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] - radius * math.sin(angle_rad)
        points.append((x, y))
    pygame.draw.polygon(screen, color, points)

def draw_bar(screen, sens, THRESHOLD_1, THRESHOLD_2):
    """感度バーを描画"""
    bar_x = (WIDTH - BAR_WIDTH) // 2
    bar_y = HEIGHT // 2
    boundary_140_x = bar_x + int((THRESHOLD_1 / 255) * BAR_WIDTH)
    boundary_220_x = bar_x + int((THRESHOLD_2 / 255) * BAR_WIDTH)

    # グレーの背景を描画
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT))
    pygame.draw.rect(screen, (169, 169, 169), (boundary_140_x, bar_y, boundary_220_x - boundary_140_x, BAR_HEIGHT))

    fill_width = int((sens / 255) * BAR_WIDTH)
    bar_color = (0, 255, 0) if sens < THRESHOLD_1 else (255, 255, 0) if sens < THRESHOLD_2 else (255, 0, 0)

    pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, BAR_HEIGHT))

    pygame.draw.line(screen, (255, 255, 255), (boundary_140_x, bar_y), (boundary_140_x, bar_y + BAR_HEIGHT - 1), 2)
    pygame.draw.line(screen, (255, 255, 255), (boundary_220_x, bar_y), (boundary_220_x, bar_y + BAR_HEIGHT - 1), 2)

def draw_circle_and_arc(screen, start_time, elapsed_time):
    """円と弧を描画"""
    pygame.draw.circle(screen, (50, 50, 50), CIRCLE_CENTER, CIRCLE_RADIUS)

    # 成功ゾーンの描画
    angle_0_2 = (TIME1 / TIME2) * 360
    angle_0_366 = 360
    fill_segment_on_arc(screen, CIRCLE_CENTER, CIRCLE_RADIUS, angle_0_2, angle_0_366, (169, 169, 169))

    # 計測中の弧の描画
    if start_time is not None:
        angle = min((elapsed_time / TIME2) * 360, 360)
        color = (255, 0, 0) if TIME1 <= elapsed_time <= TIME2 else (0, 255, 0)
        pygame.draw.arc(screen, color, 
                        (CIRCLE_CENTER[0] - CIRCLE_RADIUS, CIRCLE_CENTER[1] - CIRCLE_RADIUS, 
                         CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), 
                        0, math.radians(angle), ARC_WIDTH)

def main():
    joystick_index, axis_number, threshold, mode = select_joystick_and_axis()

    THRESHOLD_1 = 141 * (255 - threshold) / 255 + threshold
    THRESHOLD_2 = 220 * (255 - threshold) / 255 + threshold

    pygame.init()
    chroma_key = None  # 初期化しておく

    if mode == "Overlay":
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.SRCALPHA)
        hwnd = pygame.display.get_wm_info()["window"]

        # ウィンドウをレイヤードに設定
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

        # クロマキー色（ここでは (0, 0, 0)）を設定
        chroma_key = (0, 0, 0)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*chroma_key), 0, win32con.LWA_COLORKEY)

        # ウィンドウを最前面に設定
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y - int(y * 0.93), window_width, window_height, win32con.SWP_NOSIZE)

        # 最前面設定後に画面を塗りつぶす
        screen.fill(chroma_key)

    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Visible2ndStage")
        pygame_icon = pygame.image.load('./images/icon1.png')
        pygame.display.set_icon(pygame_icon)

    joystick = pygame.joystick.Joystick(joystick_index)
    joystick.init()

    sens = 0
    start_time = None
    flag = 0

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.JOYAXISMOTION and event.axis == axis_number:
                    sens = int((event.value + 1.0) / 2.0 * 255)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    pygame.quit()
                    joystick_index, axis_number, threshold, mode = select_joystick_and_axis()
                    pygame.init()

                    if mode == "Overlay":
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.SRCALPHA)
                        hwnd = pygame.display.get_wm_info()["window"]
                        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
                        chroma_key = (0, 0, 0)
                        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*chroma_key), 0, win32con.LWA_COLORKEY)
                        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y - int(y * 0.93), window_width, window_height, win32con.SWP_NOSIZE)
                        screen.fill(chroma_key)
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame_icon = pygame.image.load('./images/icon1.png')
                        pygame.display.set_icon(pygame_icon)

                    THRESHOLD_1 = 141 * (255 - threshold) / 255 + threshold
                    THRESHOLD_2 = 220 * (255 - threshold) / 255 + threshold

                    joystick = pygame.joystick.Joystick(joystick_index)
                    joystick.init()

            current_time = time.time()
            elapsed_time = 0
            if sens < THRESHOLD_1:
                start_time = None
                flag = 0
            elif THRESHOLD_1 <= sens < THRESHOLD_2:
                if start_time is None:
                    start_time = current_time
                flag = 1
                elapsed_time = current_time - start_time
            elif sens >= THRESHOLD_2 and flag == 1:
                if start_time is not None:
                    elapsed_time = current_time - start_time
                    if TIME1 <= elapsed_time <= TIME2:
                        print("SS Successed")
                        print(f"{elapsed_time:.3f} seconds\n")
                    else:
                        print("SS failed")
                        print(f"{elapsed_time:.3f} seconds\n")
                    start_time = None
                flag = 0

            # 描画処理
            screen.fill(chroma_key if mode == "Overlay" else (0, 0, 0))
            draw_bar(screen, sens, THRESHOLD_1, THRESHOLD_2)
            draw_circle_and_arc(screen, start_time, elapsed_time)

            # Overlay モードでない場合のみ sensitivity のテキストを描画
            if mode != "Overlay":
                font = pygame.font.SysFont(None, 36)
                text = font.render(f"Sensitivity: {sens}", True, (255, 255, 255))
                screen.blit(text, ((WIDTH - BAR_WIDTH) // 2, HEIGHT // 2 - 40))

                setting_font = pygame.font.SysFont(None, 24)
                setting_text = setting_font.render("s: setting", True, (255, 255, 255))
                screen.blit(setting_text, (WIDTH - setting_text.get_width() - 10, HEIGHT - setting_text.get_height() - 10))

            pygame.display.update()
            pygame.time.wait(5)

    except KeyboardInterrupt:
        print("Exiting...")
        pygame.quit()

if __name__ == "__main__":
    main()