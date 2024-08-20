import pygame


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * start + t * end


def inv_lerp(start: float, end: float, v: float) -> float:
    """Inverse Linar Interpolation, get the fraction between a and b on which v resides.
    Examples
    --------
        0.5 == inv_lerp(0, 100, 50)
        0.8 == inv_lerp(1, 5, 4.2)
    """
    return (v - start) / (end - start)


def ease_in(t):
    return t * t


def ease_out(t):
    return t * (2 - t)


def ease_in_out(t):
    return t * t * (3 - 2 * t)


def DrawRotatedWithPivot(
    surf: pygame.Surface,
    image: pygame.Surface,
    rotated_image: pygame.Surface,
    origin,
    pivot,
    angle,
):

    # offset from pivot to center
    image_rect = image.get_rect(topleft=(origin[0] - pivot[0], origin[1] - pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)

    # get a rotated image
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)


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


def render_text_to(
    font,
    surface: pygame.Surface,
    pos,
    text,
    color,
    antialias=False,
    bgcol=None,
):
    surf = font.render(text, antialias, color, bgcol)
    return surface.blit(surf, pos)
