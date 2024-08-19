import random

import pygame


from src.util import ease_in


class Particles:
    def __init__(self, color="white", lifespan=1.0) -> None:
        self.color = color
        self.lifespan = lifespan
        self.alive_since = 0

    def update(self, dt):
        killme = True
        return killme

    def draw(self, screen):
        pass


class BlockSpawnParticles(Particles):
    def __init__(self, verts: list[pygame.Vector2]) -> None:
        super().__init__(color="white", lifespan=0.5)
        self.particles: list[tuple[pygame.Vector2, pygame.Vector2]] = []
        self.wanted_radius = 3
        self.radius = self.wanted_radius
        self.orig = None

        self.spawn_particles(verts)

    def spawn_particles(self, verts: list[pygame.Vector2]):
        orig_total = pygame.Vector2()
        lines: list[list[pygame.Vector2, 2]] = []
        for i, vert in enumerate(verts):
            next_i = (i + 1) % len(verts)
            next_vert = verts[next_i]
            orig_total += vert

            lines.append([vert, next_vert])

        self.orig = orig_total / len(verts)

        for line in lines:
            start = line[0]
            end = line[1]

            point = start.copy()
            while True:
                length_left = 5

                new = point.move_towards(end, length_left)
                dis = (point - new).length()
                length_left -= dis

                particle_pos = point.copy()
                # randomize
                particle_pos += pygame.Vector2(
                    random.randint(-2, 2),
                    random.randint(-2, 2),
                )

                particle_pos_new = particle_pos.move_towards(self.orig, 5)
                _dir = particle_pos - particle_pos_new

                self.particles.append((particle_pos, _dir))
                point = new.copy()

                # end of line
                if length_left > 0:
                    break

    def draw(self, screen):
        for particle_start, _dir in self.particles:
            normalized = self.alive_since * (1 / self.lifespan)
            particle_start += _dir * normalized * 0.5
            pygame.draw.circle(screen, "white", particle_start, self.radius)

    def update(self, dt):
        self.alive_since += dt

        normalized = self.alive_since * (1 / self.lifespan)

        print(normalized)
        out = normalized * self.wanted_radius

        # invert(particle big when spawning, then smol)

        self.radius = self.wanted_radius - out

        if self.alive_since >= self.lifespan:
            return True


class ParticleManager:
    def __init__(self) -> None:
        self.particles: list[Particles] = []

    def add_spawn_fx(self, verts):
        self.particles.append(BlockSpawnParticles(verts))

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

    def update(self, dt):
        new = []
        for p in self.particles:
            should_kill = p.update(dt)
            if not should_kill:
                new.append(p)
        self.particles = new
