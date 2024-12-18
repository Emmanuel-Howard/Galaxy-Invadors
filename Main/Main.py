import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Rocks")

PLAYER_WIDTH = 100
PLAYER_HEIGHT = 120

PLAYER_VEL = 7.5
STAR_WIDTH = 30
STAR_HEIGHT = 60
STAR_VEL = 3

star_surface = pygame.Surface((STAR_WIDTH, STAR_HEIGHT))
star_surface.fill("white")  # Match the star's color

BG = pygame.image.load("maxresdefault.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
PLAYER_IMAGE = pygame.image.load("spaceship3.png")
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))

STAR_IMAGES = [
    pygame.transform.scale(pygame.image.load("turned61 (1).png"), (STAR_WIDTH, STAR_HEIGHT)),
    pygame.transform.scale(pygame.image.load("turned61 (2).png"), (STAR_WIDTH, STAR_HEIGHT)),
    pygame.transform.scale(pygame.image.load("turned61 (3).png"), (STAR_WIDTH, STAR_HEIGHT))
]
STAR_MASKS = [pygame.mask.from_surface(star) for star in STAR_IMAGES]

PLAYER_MASK = pygame.mask.from_surface(PLAYER_IMAGE)

FONT = pygame.font.SysFont("comicsans", 25)

pygame.mixer.music.load("cosmos-space-game-action-shooter-astronauts-scifi-aliens-142978.mp3")
pygame.mixer.music.play(-1)

def draw(player, elapsed_time, stars):
    WIN.blit(BG,(0,0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10,10))

    WIN.blit(PLAYER_IMAGE, (player.x, player.y))

    for star, star_type in stars:
        WIN.blit(STAR_IMAGES[star_type], (star.x, star.y))

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(400, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star_type = random.randint(0,2)
                star_rect = pygame.Rect(star_x, - STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append((star_rect, star_type))

            star_add_increment = max(250, star_add_increment - 150)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT]and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        stars_to_remove = []

        for star, star_type in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars_to_remove.append((star, star_type))

            offset = (star.x - player.x, star.y - player.y)
            if PLAYER_MASK.overlap(STAR_MASKS[star_type], offset):
                stars_to_remove.append((star, star_type))
                hit = True
                break

        stars = [star for star in stars if star not in stars_to_remove]

        if hit:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("game-over-arcade-6435.mp3")
            pygame.mixer.music.play(1)

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.music.load("game-over-160612.mp3")
            pygame.mixer.music.play(1)

            lost_text = FONT.render("GAME OVER!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(6000)
            break

        draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()



