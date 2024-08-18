from src.block import Block


class Apartment:
    def __init__(
        self,
        position,
        residents: int,
        size: tuple[int, int],
        mass: int = 40,
        degrees=0,
        friction=0.5,
        color="grey",
    ) -> None:
        self.residents = residents
        self.size = size
        self.block = Block(
            position, size, degrees, friction=friction, color=color, mass=mass
        )


class SingularApartment(Apartment):
    def __init__(self, position) -> None:
        residents = 1
        size = [36, 36]
        super().__init__(
            position,
            residents,
            size,
        )


class FamilyHome(Apartment):
    def __init__(self, position) -> None:
        residents = 3
        size = [48, 96]
        mass = 70
        super().__init__(position, residents, size, mass)


class Villa(Apartment):
    def __init__(
        self,
        position,
    ) -> None:
        residents = 8
        size = [96, 96]
        mass = 150
        friction = 0.6
        super().__init__(position, residents, size, mass, friction)


class IcyHouse(Apartment):
    def __init__(
        self,
        position,
    ) -> None:
        residents = 2
        size = [32, 32]
        mass: int = 20
        friction = 0.2
        super().__init__(position, residents, size, mass, friction, color="#5fcde4")
