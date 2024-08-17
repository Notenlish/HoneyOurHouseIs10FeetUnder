import pygame
import pymunk

from src.block import Block, StaticBlock

from src.constants import SC_HEIGHT, SC_WIDTH


class PhysicsManager:
    def __init__(self) -> None:
        self.space = pymunk.Space()
        self.space.gravity = 0,981
        self.kinematics: list[Block] = []
        self.statics = []
        
        bottom = StaticBlock([SC_WIDTH // 2, SC_HEIGHT - (10/2)], size=[SC_WIDTH, 10])
        self.add_static(bottom)
    
    def update(self, dt:float):
        self.space.step(dt)
    
    def draw_rotated_vertices(self, screen:pygame.Surface, block: Block):
        rotated = []
        for v in block.poly.get_vertices():
            vertex = v.rotated(block.body.angle) + block.body.position
            rotated.append(vertex)
        
        pygame.draw.polygon(screen, "red", rotated)
    
    def draw(self, screen:pygame.Surface):
        for arr in (self.statics, self.kinematics):
            for block in arr:
                self.draw_rotated_vertices(screen, block)
                pygame.draw.circle(screen, "blue", block.body.position, 4)
        
    def add_static(self, block:StaticBlock):
        self.statics.append(block)
        self.space.add(block.body, block.poly)
    
    def add_kinematic(self, block: Block):
        self.kinematics.append(block)
        self.space.add(block.body, block.poly)
    
    def remove_kinematic(self, block: Block):
        self.kinematics.remove(block)
        self.space.remove(block.body, block.poly)
    
        
