import pygame
import random

pygame.init()

# CONFIG
WIDTH, HEIGHT = 400, 600
LANES = 4
LANE_WIDTH = WIDTH // LANES
NOTE_SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# CORES
BG = (30, 30, 30)
GRAY = (160, 160, 160)
WHITE = (255, 255, 255)
RED = (200, 60, 60)

# TECLAS
keys = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]

# NOTAS
notes = []

class Note:
    def __init__(self, lane):
        self.lane = lane
        self.x = lane * LANE_WIDTH
        self.y = -20
        self.hit = False

    def update(self):
        self.y += NOTE_SPEED

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x + 10, self.y, LANE_WIDTH - 20, 20))

# SPAWN
def spawn_note():
    lane = random.randint(0, 3)
    notes.append(Note(lane))

spawn_timer = 0

# LOOP
running = True
while running:
    clock.tick(60)
    screen.fill(BG)

    # EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in keys:
                lane = keys.index(event.key)

                for note in notes:
                    # HIT SIMPLES
                    if note.lane == lane and abs(note.y - (HEIGHT - 100)) < 30:
                        note.hit = True

    # SPAWN AUTOMÁTICO
    spawn_timer += 1
    if spawn_timer > 40:
        spawn_note()
        spawn_timer = 0

    # DESENHAR TECLAS (CINZA)
    for i in range(LANES):
        x = i * LANE_WIDTH
        pygame.draw.rect(screen, GRAY, (x, HEIGHT - 100, LANE_WIDTH, 100))

    # LINHA DE HIT
    pygame.draw.line(screen, RED, (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)

    # ATUALIZAR NOTAS
    for note in notes[:]:
        note.update()
        note.draw()

        if note.hit or note.y > HEIGHT:
            notes.remove(note)

    pygame.display.flip()

pygame.quit()