import math

import pygame
import pymunk

from src.block import Block, StaticBlock

from src.constants import SC_HEIGHT, SC_WIDTH, DEBUG

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
    def __init__(self) -> None:
        self.space = pymunk.Space()
        self.space.gravity = 0, 981
        self.kinematics: list[Block] = []
        self.statics = []
        self.hover_obj = None

        bottom = StaticBlock([SC_WIDTH // 2, SC_HEIGHT - (10 / 2)], size=[SC_WIDTH, 10])
        self.add_static(bottom)

    def set_hover_obj(self, block: Block):
        self.hover_obj = block

    def update(self, dt: float):
        self.space.step(dt)

    def debug_draw_rotated(self, screen: pygame.Surface, block: Block):
        rotated = self.__get_rotated(block)
        pygame.draw.polygon(screen, "red", rotated)

    def __get_rotated(self, block: Block) -> list[pymunk.Vec2d]:
        rotated = []
        if type(block.poly) == pymunk.Poly:
            vertices = block.poly.get_vertices()
        else:  # circle
            vertices = []
            circle_steps = 10
            for rot in range(0, 360, 360 // circle_steps):
                rot = math.radians(rot)
                p = pymunk.Vec2d(
                    math.cos(rot) * block.poly.radius, math.sin(rot) * block.poly.radius
                )  # we only want local pos
                vertices.append(p)
        for v in vertices:
            vertex = v.rotated(block.body.angle) + block.body.position
            vertex: pymunk.Vec2d
            rotated.append(vertex)
        return rotated

    def draw_rotated(self, screen: pygame.Surface, block: Block):
        rotated = self.__get_rotated(block)
        pygame.draw.polygon(screen, block.color, rotated)
        pygame.draw.lines(screen, block.outline, True, rotated, 2)

    def draw_outline(self, screen: pygame.Surface, block: Block, time: float):
        if not block:
            return
        pygame.draw.lines(screen, "white", True, self.__get_rotated(block))
        # pov: pygame doesnt have an dashed line function and you cant figure out how to do dashed line with offset
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

    def remove_kinematic(self, block: Block):
        self.kinematics.remove(block)
        self.space.remove(block.body, block.poly)
