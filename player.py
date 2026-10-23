from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_STARTING_LIVES,
    LINE_WIDTH,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
)
import pygame

from shot import Shot


class Player(CircleShape):
    def __init__(self, x: float, y: float):
        super().__init__(x=x, y=y, radius=PLAYER_RADIUS)
        self._spawn_position = pygame.Vector2(x, y)
        self.lives = PLAYER_STARTING_LIVES
        self.respawn()

    def lose_life(self) -> None:
        if self.is_alive():
            self.lives -= 1

    def is_alive(self) -> bool:
        return self.lives > 0

    def respawn(self) -> None:
        self.position.update(self._spawn_position)
        self.velocity.update(0, 0)
        self.rotation = 0
        self.shoot_cd_timer = 0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(
            surface=screen, color="white", points=self.triangle(), width=LINE_WIDTH
        )

    def rotate(self, dt: float):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # shot cd
        self.shoot_cd_timer -= dt

    def move(self, dt: float):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shoot_cd_timer > 0:
            return

        self.shoot_cd_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
