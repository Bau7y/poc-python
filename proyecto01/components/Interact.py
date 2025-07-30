import pygame 


class Interact:
    def __init__(self, rect, name, required_item, img=None):
        request_msg = "Press E to interact",
        thanks_msg = "Thanks for the item",
        self.rect = rect
        self.name = name
        self.required_item = required_item
        self.request_msg = request_msg
        self.image = img

        self.has_requested = False

    