"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.
"""
import arcade

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class SplashView(arcade.View):
    def __init__(self, window: arcade.Window = None):
        super().__init__(window)

    def setup(self):
        pass

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("BOTTLEFIELD", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 25,
            arcade.color.WHITE, font_name='Kenney High Square', font_size=50, anchor_x="center")
        arcade.draw_text("4050", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20,
            arcade.color.WHITE, font_name='Kenney High Square', font_size=40, anchor_x="center")

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.window.show_game_view()


class GameView(arcade.View):

    def __init__(self, window: arcade.Window = None):
        super().__init__(window)

    def setup(self):
        self.bottle = self.new_bottle(SCREEN_WIDTH / 2 - 11, SCREEN_HEIGHT / 2)
        self.bottle_broken = self.new_bottle(SCREEN_WIDTH / 2 + 11, SCREEN_HEIGHT / 2, broken=True)

    def new_bottle(self, x, y, broken=False):
        if broken:
            bottle = arcade.Sprite("assets/bottle0.png", scale=0.25)
        else:
            bottle = arcade.Sprite("assets/bottle1.png", scale=0.25)
        bottle.center_x = x
        bottle.center_y = y
        return bottle

    def on_draw(self):
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, (92, 64, 51))
        self.bottle.draw()
        self.bottle_broken.draw()


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        """
        Set up the application.
        """
        super().__init__(width, height)
        self.game_view = GameView(self)
        self.splash_view = SplashView(self)

    def setup(self):
        self.show_splash_view()

    def show_game_view(self):
        self.game_view.setup()
        self.show_view(self.game_view)

    def show_splash_view(self):
        self.splash_view.setup()
        self.show_view(self.splash_view)


def main():
    arcade.enable_timings()
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
