from typing import TYPE_CHECKING

from src.block import Block

if TYPE_CHECKING:
    from main import App


class Game:
    def __init__(self, app: "App") -> None:
        self.app = app
        self.highscore = 0
        self.physics = self.app.physics

    def spawn_block(self, mpos:tuple[int, int]):
        block = Block(mpos, [20,20], degrees=44)
        self.physics.add_kinematic(block)