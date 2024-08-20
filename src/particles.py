from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App


import random

import pygame


from src.util import ease_in
from src.amsa_particles import ParticleBox


class Particles:
    def __init__(self, color="white", lifespan=0.5) -> None:
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
        super().__init__(color="white", lifespan=0.8)
        self.particles: list[tuple[pygame.Vector2, pygame.Vector2]] = []
        self.wanted_radius = 6
        self.radius = self.wanted_radius
        self.orig = None
        self.move_speed = 1

        # self.spawn_amsa_particles(verts)
        self.spawn_particles(verts)

    def spawn_amsa_particles(self, verts: list[pygame.Vector2]):
        self.pbs = [
            ParticleBox(
                rect=(-10, 540, 800, 60),
                shape="circle",
                color=[[x + 128, x + 128, x + 128, 255] for x in range(127)],
                lifetime=3,
                vel=[(0, -50), (0, -100), "minmax"],
                size=[15, 15],
                angle=0,
                size_overtime=[[(0, 0), 1]],
            ),
        ]

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
                if _dir.length():
                    _dir = _dir.normalize()

                self.particles.append((particle_pos, _dir))
                point = new.copy()

                # end of line
                if length_left > 0:
                    break

    def draw(self, screen):
        for particle_start, _dir in self.particles:
            normalized = self.alive_since * (1 / self.lifespan)
            particle_start += _dir * normalized * self.move_speed
            pygame.draw.circle(screen, self.color, particle_start, self.radius)

    def update(self, dt):
        self.alive_since += dt

        normalised = self.alive_since * (1 / self.lifespan)
        normalised = min(max(normalised, 0), 1)
        inv_normalised = 1.0 - normalised

        half_lifespan = self.lifespan * 0.5
        if normalised <= half_lifespan:
            out = normalised * 2
        else:
            out = self.lifespan - (normalised - half_lifespan) * 2

        normalised * self.wanted_radius

        self.radius = self.wanted_radius * out

        base = pygame.Color(255, 255, 255)
        addition = pygame.Color([normalised * 75] * 3)
        self.color = base - addition

        if self.alive_since >= self.lifespan:
            return True


class ParticleManager:
    def __init__(self, app: "App") -> None:
        self.app = app
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
