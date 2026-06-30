import math
import random
import pygame
import matplotlib.pyplot as plt

N_NODES = 7              
SPEED = 60.0             
DT = 0.1                 
STEPS = 100              
NODE_RADIUS = 8          
COLLISION_DIST = NODE_RADIUS * 2   

START_W, START_H = 100, 50    
STEP_W, STEP_H = 50, 50        
NUM_EXPERIMENTS = 10         

FPS = 60                       
MAX_DISPLAY = 600            


def build_window_sizes():
    sizes = []
    w, h = START_W, START_H
    for _ in range(NUM_EXPERIMENTS):
        sizes.append((w, h))
        w += STEP_W
        h += STEP_H
    return sizes


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        self.vx = SPEED * math.cos(angle)
        self.vy = SPEED * math.sin(angle)

    def step(self, w, h):
      
        if random.random() < 0.15:
            angle = random.uniform(0, 2 * math.pi)
            self.vx = SPEED * math.cos(angle)
            self.vy = SPEED * math.sin(angle)

        self.x += self.vx * DT
        self.y += self.vy * DT

        if self.x - NODE_RADIUS < 0:
            self.x = NODE_RADIUS
            self.vx *= -1
        if self.x + NODE_RADIUS > w:
            self.x = w - NODE_RADIUS
            self.vx *= -1
        if self.y - NODE_RADIUS < 0:
            self.y = NODE_RADIUS
            self.vy *= -1
        if self.y + NODE_RADIUS > h:
            self.y = h - NODE_RADIUS
            self.vy *= -1


def run_experiment(w, h, screen, font, exp_index, total):

    nodes = [Node(random.uniform(NODE_RADIUS, w - NODE_RADIUS),
                   random.uniform(NODE_RADIUS, h - NODE_RADIUS))
              for _ in range(N_NODES)]

    collision_count = 0
    was_colliding = set()   

    # scale factor so the logical window fits inside the fixed screen
    scale = min(MAX_DISPLAY / w, MAX_DISPLAY / h, 1.0)

    clock = pygame.time.Clock()

    for step in range(STEPS):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # move nodes
        for node in nodes:
            node.step(w, h)

        # collision check (pairwise)
        now_colliding = set()
        for i in range(N_NODES):
            for j in range(i + 1, N_NODES):
                dx = nodes[i].x - nodes[j].x
                dy = nodes[i].y - nodes[j].y
                dist = math.hypot(dx, dy)
                if dist <= COLLISION_DIST:
                    pair = (i, j)
                    now_colliding.add(pair)
                    if pair not in was_colliding:
                        collision_count += 1   # count only new collision events
        was_colliding = now_colliding

        # draw 
        screen.fill((10, 10, 18))

        # draw window boundary (scaled)
        rect_w, rect_h = int(w * scale), int(h * scale)
        pygame.draw.rect(screen, (60, 60, 90), (0, 0, rect_w, rect_h), 1)

        for node in nodes:
            sx, sy = int(node.x * scale), int(node.y * scale)
            r = max(2, int(NODE_RADIUS * scale))
            pygame.draw.circle(screen, (80, 200, 255), (sx, sy), r)

        for (i, j) in now_colliding:
            pygame.draw.line(
                screen, (255, 80, 80),
                (nodes[i].x * scale, nodes[i].y * scale),
                (nodes[j].x * scale, nodes[j].y * scale), 2)

        info_lines = [
            f"Experiment: {exp_index+1}/{total}",
            f"Window: {w} x {h}  (Area={w*h})",
            f"Step: {step+1}/{STEPS}",
            f"Collisions: {collision_count}",
        ]
        for idx, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (5, 5 + idx * 18))

        pygame.display.flip()
        clock.tick(FPS)

    return collision_count


def main():
    pygame.init()
    font = pygame.font.SysFont("consolas", 16)

    screen = pygame.display.set_mode((MAX_DISPLAY, MAX_DISPLAY))
    pygame.display.set_caption("Bounded Random Walk Collision Simulation")

    window_sizes = build_window_sizes()
    results = []  # list of (area, collision_count, w, h)

    for idx, (w, h) in enumerate(window_sizes):
        collisions = run_experiment(w, h, screen, font, idx, len(window_sizes))
        area = w * h
        results.append((area, collisions, w, h))
        print(f"[{idx+1}/{len(window_sizes)}] Window {w}x{h} -> Area={area}, Collisions={collisions}")

    pygame.quit()

    # final graph 
    areas = [r[0] for r in results]
    collisions = [r[1] for r in results]

    plt.figure(figsize=(9, 5))
    plt.plot(areas, collisions, marker="o", markersize=3, color="crimson", linewidth=1.5)

    plt.title(f"Window Area vs Collision Count\n(N={N_NODES} nodes, fixed speed, {STEPS} steps, {NUM_EXPERIMENTS} window sizes)")
    plt.xlabel("Window Area (logical units^2)")
    plt.ylabel("Collision Count")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("area_vs_collision.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()