import pygame

class Buttons:
    def __init__(self, x, y, image_normal, image_hover, scale=1):
        self.image = pygame.transform.scale(image_normal, (
            int(image_normal.get_width() * scale),
            int(image_normal.get_height() * scale)
        ))
        self.image_hover = pygame.transform.scale(image_hover, (
            int(image_hover.get_width() * scale),
            int(image_hover.get_height() * scale)
        ))
        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False


    
    def draw(self, screen):
        pos = pygame.mouse.get_pos() # posicion del mouse

        if self.rect.collidepoint(pos):
            self.image = self.image_hover
        else:
            self.image = self.image_normal

        screen.blit(self.image, self.rect)
        

    def clicked(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True
        return False
