import pygame
import sys
import random

# تنظیمات صفحه نمایش
WIDTH = 800
HEIGHT = 600
FPS = 60

# تنظیمات رنگ
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# ماشین
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("benz_car.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 50)
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def move(self, direction):
        if direction == "left":
            self.speed_x = -12
        elif direction == "right":
            self.speed_x = 12
        else:
            self.speed_x = 0

# مانع
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bmw_car.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y += 1  # افزایش سرعت حرکت موانع به تدریج

# مرحله بازی
def game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ماشین‌ها")
    clock = pygame.time.Clock()

    pygame.mixer.init()
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    car = Car()
    all_sprites.add(car)

    for _ in range(8):
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car.move("left")
                elif event.key == pygame.K_RIGHT:
                    car.move("right")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and car.speed_x < 0:
                    car.move("")
                elif event.key == pygame.K_RIGHT and car.speed_x > 0:
                    car.move("")

        all_sprites.update()

        # بررسی برخورد ماشین با موانع
        hits = pygame.sprite.spritecollide(car, obstacles, False)
        if hits:
            running = False

        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

game()