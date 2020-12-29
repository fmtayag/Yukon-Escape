import pygame

def draw_background(surf, img, img_rect, pos, direction="vertical"):
    if direction == "vertical":
        surf_h = surf.get_height()
        rel_y = pos % img_rect.height
        surf.blit(img, (0, rel_y - img_rect.height))

        if rel_y < surf_h:
            surf.blit(img, (0, rel_y))

    elif direction == "horizontal":
        surf_w = surf.get_width()
        rel_x = pos % img_rect.width
        surf.blit(img, (rel_x - img_rect.width, 0))

        if rel_x < surf_w:
            surf.blit(img, (rel_x, 0))

def draw_text(surf, text, size, font, x, y, color, align="normal"):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "centered":
        text_rect.centerx = x
        text_rect.y = y
    elif align == "normal":
        text_rect.x = x
        text_rect.y = y
    surf.blit(text_surface, (text_rect.x, text_rect.y))

def shake(intensity, n):
    # Credits to sloth from StackOverflow, thanks buddy!
    shake = -1
    for _ in range(n):
        for x in range(0, intensity, 5):
            yield (x*shake, 0)
        for x in range(intensity, 0, 5):
            yield (x*shake, 0)
        shake *= -1
    while True:
        yield (0, 0)

def draw_shadows(shadows_list):
    for shadow in shadows_list:
        shadow.draw()

        if shadow.Caster.impacted:
            shadows_list.remove(shadow)
            del shadow

def draw_bouncies(bouncies):
    for b in bouncies:
        b.draw()

def draw_particles(particles_list):
    for p in particles_list:
        p.draw()

        if (p.x < -p.size or
            p.x > p.WIN_RES["W"] + p.size or
            p.y < -p.size or
            p.y > p.WIN_RES["H"] + p.size):
                particles_list.remove(p)
                del p
