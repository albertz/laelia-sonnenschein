"""
Sonnenschein
"""

# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


class Character:
    def __init__(self, name, pos: pygame.Vector2, gfx_path: str):
        self.name = name
        self.pos = pos
        self.gfx = pygame.image.load(gfx_path)
        self.gfx = pygame.transform.smoothscale(self.gfx, (100, 100))
        # Add alpha channel to gfx
        self.gfx = self.gfx.convert_alpha()
        # Make white (up to threshold) to transparent
        for x in range(self.gfx.get_width()):
            for y in range(self.gfx.get_height()):
                color = self.gfx.get_at((x, y))
                if color[0] > 200 and color[1] > 200 and color[2] > 200:
                    color = (255, 255, 255, 0)
                self.gfx.set_at((x, y), color)

    def handle_keys(self, keys):
        if keys[pygame.K_UP]:
            self.move(0, -300 * dt)
        if keys[pygame.K_DOWN]:
            self.move(0, 300 * dt)
        if keys[pygame.K_LEFT]:
            self.move(-300 * dt, 0)
        if keys[pygame.K_RIGHT]:
            self.move(300 * dt, 0)

    def handle_ai_move_towards(self, target_pos: pygame.Vector2):
        # Move towards target
        direction = target_pos - self.pos
        if direction.length() < 100:
            return
        direction.normalize_ip()
        self.move(direction.x * 200 * dt, direction.y * 200 * dt)

    def move(self, x, y):
        self.pos.x += x
        self.pos.y += y

    def draw(self):
        # Draw gfx
        screen.blit(self.gfx, self.pos - pygame.Vector2(self.gfx.get_width() / 2, self.gfx.get_height() / 2))

        # Check if player out of screen (left,right,top,down)
        if self.pos.x < 0 or self.pos.x > screen.get_width() or self.pos.y < 0 or self.pos.y > screen.get_height():
            # Print arrow in that direction on the edge of the screen
            edge_pos = pygame.Vector2(self.pos)
            if self.pos.x < 0:
                edge_pos.x = 0
            elif self.pos.x > screen.get_width():
                edge_pos.x = screen.get_width()
            if self.pos.y < 0:
                edge_pos.y = 0
            elif self.pos.y > screen.get_height():
                edge_pos.y = screen.get_height()
            pygame.draw.circle(screen, "gray", edge_pos, 5)


class Area:
    def __init__(self, name: str, pos: pygame.Vector2, size: pygame.Vector2, color: str):
        self.name = name
        self.pos = pos
        self.size = size
        self.color = color

    def draw(self):
        # fill rect
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos, self.size))


players = [
    Character("Girl", pygame.Vector2(100, 300), "assets/girl1.jpeg"),
    Character("Yellow mouse", pygame.Vector2(100, 100), "assets/mouse3.jpeg"),
    Character("Elephant", pygame.Vector2(300, 300), "assets/elephant1.jpeg"),
    # Character("Fat mouse", pygame.Vector2(200, 200), "assets/mouse4.jpeg"),
    Character("Med mouse", pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), "assets/mouse2.jpeg"),
    Character("Duck", pygame.Vector2(500, 100), "assets/duck1.jpeg"),
    # Character("Dragon", pygame.Vector2(600, 200), "assets/dragon1.jpeg"),
    Character("Black socks", pygame.Vector2(500, 100), "assets/socks.jpeg"),
]
areas = [
    Area("sky", pygame.Vector2(0, 0), pygame.Vector2(screen.get_width(), screen.get_height() / 2), "skyblue"),
    Area(
        "ground",
        pygame.Vector2(0, screen.get_height() / 2),
        pygame.Vector2(screen.get_width(), screen.get_height() / 2),
        "gray",
    ),
]


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # human_player.handle_keys(keys)

    players[0].handle_keys(keys)

    for i in range(1, len(players)):
        target_pos = players[i - 1].pos.copy()
        players[i].handle_ai_move_towards(target_pos)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for area in areas:
        area.draw()
    for player in players:
        player.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
