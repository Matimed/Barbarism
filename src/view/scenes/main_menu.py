from view.scenes import Scene


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        Scene.window.set_background((255,255,255))


    def actualizar(self, eventos):
        Scene.window.update()