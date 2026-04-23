import arcade

class Gameplay(arcade.Window):
    def __init__(
        self, 
        width = 1280, 
        height = 720, 
        title = "Arcade Window", 
        fullscreen = False, 
        resizable = False
        ):
        
        super().__init__(
            width, 
            height, 
            title, 
            fullscreen, 
            resizable, 
        )