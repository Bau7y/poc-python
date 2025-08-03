import pygame 


class Interact:
    def __init__(self, rect, name, required_item, img=None, request_msg = "Press E to interact",
        thanks_msg = "Thanks for the item",):
        self.rect = rect
        self.name = name
        self.required_item = required_item
        self.thanks_msg = thanks_msg
        self.request_msg = request_msg
        self.image = img

        self.has_requested = False  
        self.completed = False
        self.enabled = True
        self.visible = True

        self.block_rect = rect.copy()

    def draw(self, screen, scroll_x, scroll_y):
        if self.visible and self.image:
            screen.blit(self.image, (self.rect.x - scroll_x, self.rect.y - scroll_y))

    def try_interact(self, player):
        if not self.enabled:
            return False

        if player.has_item(self.required_item):
            if not self.enabled:
                return None
            
            #primer request
            if not self.has_requested:
                self.has_requested = True
                return f"{self.name}: {self.request_msg}"
            
            #pedido, agregar 
            if player.has_item(self.required_item):
                player.remove_item(self.required_item, 1)
                self.completed = True
                self.enabled = False
                self.visible = False

                if hasattr(player, "obstaculos") and self.block_rect in player.obstaculos:
                    player.obstaculos.remove(self.block_rect)
                return f"{self.name}: {self.thanks_msg}"
            return f"Aún necesito {self.required_item}"