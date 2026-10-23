import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    clock = pygame.time.Clock()
    dt = 0.0

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    # game loop
    while True:
        log_state()

        # properly quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        player.draw(screen=screen)
        player.update(dt)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
