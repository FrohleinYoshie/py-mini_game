import pygame
import sys

# 初期化
pygame.init()

# 画面サイズ
screen_width = 400
screen_height = 400

# 色
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

# ボタンのサイズ
button_width = 100
button_height = 100

# ボタンのマージン
margin = 5

# ボタンの初期状態
button_states = [[black for _ in range(3)] for _ in range(3)]

# 画面作成
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("クリックゲーム")

# ボタンの位置を計算する関数
def calculate_button_position(row, col):
    x_offset = (screen_width - (button_width * 3 + margin * 2)) // 2
    y_offset = (screen_height - (button_height * 3 + margin * 2)) // 2
    x = x_offset + col * (button_width + margin)
    y = y_offset + row * (button_height + margin)
    return x, y

# ボタンを描画する関数
def draw_buttons():
    for row in range(3):
        for col in range(3):
            x, y = calculate_button_position(row, col)
            pygame.draw.rect(screen, button_states[row][col], (x, y, button_width, button_height))

# ゲーム画面
def game_screen():
    screen.fill(white)
    draw_buttons()
    pygame.display.flip()

# ボタンを切り替える関数
def toggle_buttons(row, col):
    button_states[row][col] = yellow if button_states[row][col] == black else black

    if row > 0:
        button_states[row - 1][col] = yellow if button_states[row - 1][col] == black else black
    if row < 2:
        button_states[row + 1][col] = yellow if button_states[row + 1][col] == black else black
    if col > 0:
        button_states[row][col - 1] = yellow if button_states[row][col - 1] == black else black
    if col < 2:
        button_states[row][col + 1] = yellow if button_states[row][col + 1] == black else black

# スタート画面
def start_screen():
    screen.fill(white)
    start_button_rect = pygame.Rect(100, 150, 200, 50)
    pygame.draw.rect(screen, black, start_button_rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Game Start", True, white)
    text_rect = text_surface.get_rect(center=start_button_rect.center)
    screen.blit(text_surface, text_rect)

    # 説明文の描画
    explanation_font = pygame.font.Font(None, 24)
    explanation_text = "Click to turn all buttons yellow"
    explanation_surface = explanation_font.render(explanation_text, True, black)
    explanation_rect = explanation_surface.get_rect(center=(screen_width // 2, start_button_rect.y + 70))
    screen.blit(explanation_surface, explanation_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    return


# ゲームクリアフラグ
game_clear = False
mouse_x = 0  # 初期化
mouse_y = 0  # 初期化

# メインループ
# スタート画面を表示
start_screen()

# ゲーム画面を表示
game_screen()

# ゲームループ
while True:
    for event in pygame.event.get():
        # イベント処理: ウィンドウを閉じたときの処理
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # イベント処理: マウスクリック時の処理
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # ゲームクリア時の処理
            if game_clear:
                if (mouse_x, mouse_y):
                    # ゲームクリア状態をリセットして、ボタンの初期状態に戻す
                    game_clear = False
                    button_states = [[black for _ in range(3)] for _ in range(3)]
                    game_screen()

            else:
                # ボタンがクリックされたかどうかを判定し、ボタンの状態を切り替える
                for row in range(3):
                    for col in range(3):
                        x, y = calculate_button_position(row, col)
                        if x <= mouse_x < x + button_width and y <= mouse_y < y + button_height:
                            toggle_buttons(row, col)
                game_screen()

                # 全てのボタンが黄色かどうかをチェックし、ゲームクリア状態にする
                all_yellow = all(button_states[row][col] == yellow for row in range(3) for col in range(3))
                if all_yellow:
                    game_clear = True
                    font = pygame.font.Font(None, 36)
                    # ゲームクリアメッセージの表示
                    text_surface = font.render("Game Clear", True, black)
                    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
                    screen.blit(text_surface, text_rect)
                    # リプレイボタンの表示
                    return_button_rect = pygame.Rect(150, 250, 100, 50)
                    pygame.draw.rect(screen, black, return_button_rect)
                    text_surface = font.render("Replay", True, white)
                    text_rect = text_surface.get_rect(center=return_button_rect.center)
                    screen.blit(text_surface, text_rect)
                    pygame.display.flip()
