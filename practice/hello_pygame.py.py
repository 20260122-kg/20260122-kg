import pygame
import sys
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Game")

# 색상
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PEACH = (255, 218, 185)  # 살구색

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)

# 플레이어
player_size = 60
x, y = 300, 300
base_speed = 5

enemies = []
game_over = False

start_time = time.time()

def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        ex = random.randint(0, WIDTH)
        ey = 0
        dx, dy = random.uniform(-2, 2), random.uniform(2, 5)
    elif side == "bottom":
        ex = random.randint(0, WIDTH)
        ey = HEIGHT
        dx, dy = random.uniform(-2, 2), random.uniform(-5, -2)
    elif side == "left":
        ex = 0
        ey = random.randint(0, HEIGHT)
        dx, dy = random.uniform(2, 5), random.uniform(-2, 2)
    else:
        ex = WIDTH
        ey = random.randint(0, HEIGHT)
        dx, dy = random.uniform(-5, -2), random.uniform(-2, 2)

    enemies.append([ex, ey, dx, dy])

def reset_game():
    global x, y, enemies, game_over, start_time
    x, y = 300, 300
    enemies = []
    game_over = False
    start_time = time.time()

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 🔥 Retry 버튼 클릭
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if retry_rect.collidepoint(mouse_pos):
                reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()

        speed = base_speed
        if keys[pygame.K_LSHIFT]:
            speed = base_speed * 3

        if keys[pygame.K_w]:
            y -= speed
        if keys[pygame.K_s]:
            y += speed
        if keys[pygame.K_a]:
            x -= speed
        if keys[pygame.K_d]:
            x += speed

        # 화면 제한
        x = max(0, min(WIDTH - player_size, x))
        y = max(0, min(HEIGHT - player_size, y))

        # 적 생성
        if random.random() < 0.03:
            spawn_enemy()

        # 적 이동
        for enemy in enemies:
            enemy[0] += enemy[2]
            enemy[1] += enemy[3]

        # 충돌 체크
        player_rect = pygame.Rect(x, y, player_size, player_size)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0] - 10, enemy[1] - 10, 20, 20)
            if player_rect.colliderect(enemy_rect):
                game_over = True

    # 🎨 배경 (잔상 없음)
    screen.fill(PEACH)

    # 플레이어 (잔상 효과 유지하고 싶으면 따로 처리 가능)
    pygame.draw.rect(screen, BLUE, (int(x), int(y), player_size, player_size))

    # 🔴 적 (잔상 없음 → 그냥 바로 그림)
    for enemy in enemies:
        pygame.draw.circle(screen, RED, (int(enemy[0]), int(enemy[1])), 10)

    # ⏱ 점수 (시간)
    if not game_over:
        score = int(time.time() - start_time)
    score_text = small_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # 💥 게임 오버 UI
    if game_over:
        text = font.render("Game Over!", True, (0, 0, 0))
        screen.blit(text, (180, 200))

        # 🔘 Retry 버튼
        retry_rect = pygame.Rect(220, 300, 160, 50)
        pygame.draw.rect(screen, BLUE, retry_rect)

        retry_text = small_font.render("Retry", True, WHITE)
        screen.blit(retry_text, (270, 315))

    pygame.display.flip()

pygame.quit()
sys.exit()