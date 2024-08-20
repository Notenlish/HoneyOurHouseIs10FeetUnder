from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App

import math

import pygame
import pymunk

from src.block import Block, StaticBlock

from src.constants import SC_HEIGHT, SC_WIDTH, DEBUG, WEB, CACHE, COLLTYPE_GROUND
from src.util import blitRotate
from src.collision_handler import CollisionHandler

import time


def aaa(self, screen, block, time):
    if not block:
        return
    line_gap = 5
    rotated = self.__get_rotated(block)
    offset = time
    line_count = 0
    v = line_gap
    for i, point in enumerate(rotated):
        point = pygame.Vector2(*point)

        next_i = (i + 1) % len(rotated)
        next_point = pygame.Vector2(*rotated[next_i])

        point.move_towards_ip(next_point, offset)

        start = point.copy()
        while True:
            if v == 0:
                # start a new dash/empty gap
                line_left = line_gap
            else:
                # continue from the old one
                line_left = v
                line_count -= 1  # make it so its the same color

            end = start.move_towards(next_point, line_left)
            dist = start - end
            line_left -= dist.length()
            line_left = round(line_left)  # get rid of float inconsistency

            if line_count % 2:
                color = "white"
            else:
                color = "black"
            pygame.draw.line(screen, color, start, end)

            start = end.copy()  # I hope this doesnt do memory leak

            # instead of this, it should check for length
            # basically, create a new var called `line_left`
            # and subtract from it the length of the dist of start to end
            # if the length is more than 0, dont reset line_left draw etc.
            if start.xy == next_point.xy:
                break
            # print(
            # f"lineleft: {line_left}  v:{v} start:{start} end{end} next point{next_point}"
            # )

            v = line_left
            line_count += 1

        if i == len(rotated):
            break

        i += 1


class PhysicsManager:
    def __init__(self, app: "App") -> None:
        self.app = app
        self.camera = app.camera
        self.space = pymunk.Space()
        self.space.gravity = 0, 981

        if WEB:
            # 10% more perf :D
            self.space.iterations = 9
        # TODO: if web performance drops, allow user to tweak space.iterations property
        # TODO: maybe enable this?
        self.space.sleep_time_threshold = 2.0

        self.coll_handler = CollisionHandler(self)

        self.kinematics: list[Block] = []
        self.statics = []
        self.hover_obj = None

        # get rid of weird inconsistency
        bottom = StaticBlock(
            position=[SC_WIDTH // 2 + 1, SC_HEIGHT - (100 / 2) + 4],
            size=[SC_WIDTH, 50],
            sprite_name="ground.png",
            collision_type=COLLTYPE_GROUND,
        )
        self.add_static(bottom)

        self.circle_vertex_count = 15
        self.circle_normalized_points = [
            pymunk.Vec2d(math.cos(math.radians(rot)), math.sin(math.radians(rot)))
            for rot in range(0, 360, 360 // self.circle_vertex_count)
        ]

    def set_hover_obj(self, block: Block):
        self.hover_obj = block

    def update(self, dt: float):
        self.space.step(dt)

        self.check_dynamic(dt)

    def check_dynamic(self, dt):
        lost = True
        game_rect = self.camera.get_game_rect()

        if not self.app.game.started:
            lost = False
        for kinematic in self.kinematics:
            # dont keep objects that have fallen off
            if kinematic.body.position.y > 9999:
                self.remove_kinematic(kinematic)

            if self.check_block_visible(kinematic, game_rect):
                lost = False

            kinematic.update(dt)
        if lost:
            print("lost :////")
            self.app.game.end()

    def check_block_visible(self, block: Block, game_rect: pygame.Rect):
        if game_rect.collidepoint(block.body.position):
            return True
        return False

    def debug_draw_rotated(self, screen: pygame.Surface, block: Block):
        rotated = self.__get_rotated(block)
        pygame.draw.polygon(screen, "red", rotated)

    def __get_rotated(self, block: Block) -> list[pymunk.Vec2d]:
        rotated = []
        if type(block.poly) == pymunk.Poly:
            vertices = block.poly.get_vertices()
        else:  # circle
            vertices = []
            for v in self.circle_normalized_points:
                vertices.append(v * block.poly.radius)

        for v in vertices:
            vertex = v.rotated(block.body.angle) + block.body.position
            rotated.append(self.camera.to_display(vertex))
        return rotated

    def draw_rotated(self, screen: pygame.Surface, block: Block):
        rotated = self.__get_rotated(block)
        # pygame.draw.polygon(screen, block.color, rotated)
        # pygame.draw.lines(screen, block.outline, True, rotated, 2)

        if block.shape_type != "circle":
            pos = (block.poly.bb.left, block.poly.bb.bottom)
            screen.blit(block.get_spr(), self.camera.to_display(pos))
        else:
            # DrawRotatedWithPivot()
            rotated = block.get_spr()
            og, angle = CACHE.get_cache(block.sprite_name, block.spr_size_mul, 0)
            blitRotate(
                screen,
                og,
                rotated,
                self.camera.to_display(block.body.position),
                og.get_rect().center,
                angle,
            )

        if block.body.is_sleeping and DEBUG:
            pygame.draw.circle(
                screen, block.outline, self.camera.to_display(block.body.position), 5
            )

    def draw_outline(self, screen: pygame.Surface, block: Block, time: float):
        if not block:
            return
        pygame.draw.lines(screen, "white", True, self.__get_rotated(block))
        # pov: pygame doesnt have an dashed line function and you cant
        # figure out how to do dashed line with offset
        return
        line_gap = 5
        rotated = self.__get_rotated(block)
        # rotated = [[10, 10], [200, 10], [200, 200], [10, 200]]
        lines: list[tuple[pygame.Vector2, pygame.Vector2]] = []

        for i, point in enumerate(rotated):
            next_point = rotated[(i + 1) % len(rotated)]
            point = pygame.Vector2(*point)
            next_point = pygame.Vector2(*next_point)
            lines.append((point, next_point))

        offset = 0  # dont use offset, broken.
        # print(offset)
        segments = []
        line_index = 0
        length_left = line_gap
        segment_i = 0

        start = lines[line_index][0]
        veryright = lines[line_index][1]

        start.move_towards_ip(veryright, offset)
        print(start)

        segment = {"positions": [start]}
        segment_pos = start
        first_start = start.copy()
        while True:
            line = lines[line_index]

            left = line[0]
            right = line[1]

            start = segment_pos.copy()
            end = start.move_towards(right, length_left)

            distance = (start - end).length()
            length_left -= distance

            segment_i += 1

            # the segment cant go any further in this line
            if length_left <= 0:
                segment["positions"].append(end)
                segment["i"] = segment_i
                # print(segment_i)
                segments.append(segment)
                # print("segment finished, creating new segment")

                # start back from the last point
                segment_pos = end
                segment = {"positions": [start]}
                length_left = line_gap
                # its in an infinite loop
                # this is because when it iterates to the next element, the start and end are still the same
                # we need to find a way to store where the segment ended so we can use it in the next iteration
            else:
                # segment can move on to the next line
                segment["positions"].append(end)
                # print("segment not done")
                line_index += 1

                # print(line_index, first_start, segment_pos, line_gap, offset)
                if line_index >= 1 and (first_start - segment_pos).length() < line_gap:
                    break
                if line_index >= len(rotated):
                    break
                line = lines[line_index]
                left = line[0]
                segment_pos = left.copy()
                segment_i -= 1
                continue
        # basically, generate a list of segments that contain whether they're solid or not
        # then, after getting the list segments, loop over them, check for length_left and if its 0 or lower,
        # then continue to the next segment
        # if there's length_left(after completing a particular side)
        # then just dont get the next segment and instead get the next vertex

        # print("---")
        for segment in segments:
            positions: list[pygame.Vector2] = segment["positions"]
            positions: list[tuple[int, int]] = [(pos.x, pos.y) for pos in positions]
            segment_i = segment["i"]
            # print(segment_i)
            if segment_i % 4 == 1:
                pygame.draw.lines(screen, "white", False, positions)

    def draw(self, screen: pygame.Surface, time: float):
        if DEBUG:
            for arr in (self.statics, self.kinematics):
                for block in arr:
                    self.debug_draw_rotated(screen, block)
                    pygame.draw.circle(screen, "blue", block.body.position, 4)
        else:
            for arr in (self.statics, self.kinematics):
                for block in arr:
                    self.draw_rotated(screen, block)
                    # pygame.draw.circle(screen, "white", block.body.position, 3)

        self.draw_outline(screen, self.hover_obj, time)

    def add_static(self, block: StaticBlock):
        self.statics.append(block)
        self.space.add(block.body, block.poly)

    def add_kinematic(self, block: Block):
        self.kinematics.append(block)
        self.space.add(block.body, block.poly)

        self.app.particle_manager.add_spawn_fx(self.__get_rotated(block))

    def remove_kinematic(self, block: Block):
        self.kinematics.remove(block)
        self.space.remove(block.body, block.poly)
