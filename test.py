import pygame


screen = pygame.display.set_mode((100, 100), pygame.SCALED | pygame.RESIZABLE)
clock = pygame.time.Clock()

spr = pygame.image.load("assets/block/plastic_circle.png").convert()
spr.set_colorkey("#000000")


def blitRotate(
    surf: pygame.Surface,
    image: pygame.Surface,
    rotated_image: pygame.Surface,
    pos,
    originPos,
    angle,
):
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = rotated_image  # pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)


time = 0
while True:
    screen.fill("white")
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            raise SystemExit

    angle = time * 2

    inp = pygame.transform.rotozoom(spr, angle, 1.0)
    inp2 = pygame.transform.scale_by(pygame.transform.rotate(spr, angle), 1.0)
    blitRotate(
        screen,
        spr,
        inp2,
        (50, 50),
        (36, 36),
        angle,
    )
    dt = clock.tick(60) / 1000
    time += dt
    pygame.display.update()
