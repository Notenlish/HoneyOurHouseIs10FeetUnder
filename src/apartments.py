from src.block import Block


class Apartment:
    def __init__(
        self,
        position,
        residents: int,
        size: tuple[int, int],
        spr=None,
        mass: int = 40,
        degrees=0,
        friction=0.5,
        color="grey",
    ) -> None:
        self.residents = residents
        self.size = size
        self.block = Block(
            position,
            size,
            degrees,
            friction=friction,
            color=color,
            mass=mass,
            sprite_name=spr,
        )


class SingularApartment(Apartment):
    def __init__(self, position, degrees=0) -> None:
        residents = 1
        size = [36, 36]
        super().__init__(position, residents, size, degrees=degrees, spr="singular.png")


class FamilyHome(Apartment):
    def __init__(self, position, degrees=0) -> None:
        residents = 3
        size = [48, 96]
        mass = 70
        super().__init__(
            position, residents, size, mass, degrees=degrees, spr="family_house.png"
        )


class Villa(Apartment):
    def __init__(self, position, degrees=0) -> None:
        residents = 8
        size = [48, 96]
        mass = 150
        friction = 0.6
        super().__init__(
            position, residents, size, mass, friction, degrees=degrees, spr="villa.png"
        )


class IcyHouse(Apartment):
    def __init__(self, position, degrees=0) -> None:
        residents = 2
        size = [32, 32]
        mass: int = 20
        friction = 0.2
        super().__init__(
            position, residents, size, mass, friction, degrees=degrees, color="#5fcde4"
        )
