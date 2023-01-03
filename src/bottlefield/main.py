"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.
"""
import arcade
import random

FIELD_WIDTH, FIELD_HEIGHT = 20, 7

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
        self.window.set_mouse_visible(False)
        self.bottle = self.new_bottle(SCREEN_WIDTH / 2 - 11, SCREEN_HEIGHT / 2)
        self.bottle_broken = self.new_bottle(SCREEN_WIDTH / 2 + 11, SCREEN_HEIGHT / 2, broken=True)
        self.bottle_list = arcade.SpriteList()
        self.broken_bottle_list = arcade.SpriteList()

        self.bottle_sound = arcade.load_sound("assets/glass-breaking.wav")
        self.mouse_pos = (0, 0)
        self.generate_field()

    def generate_field(self):
        shift_lim_x = 15
        shift_lim_y = 15
        padding_x = (SCREEN_WIDTH // FIELD_WIDTH) // 2
        padding_y = (SCREEN_HEIGHT // FIELD_HEIGHT) // 2
        for y in range(padding_y, SCREEN_HEIGHT, SCREEN_HEIGHT // FIELD_HEIGHT):
            for x in range(padding_x, SCREEN_WIDTH, SCREEN_WIDTH // FIELD_WIDTH):
                rotation = random.randint(0, 11) * 30
                shift_x = random.randint(-shift_lim_x, shift_lim_x)
                shift_y = random.randint(-shift_lim_y, shift_lim_y)
                if random.randint(0, 1) == 0:
                    self.bottle_list.append(self.new_bottle(x + shift_x, y + shift_y, angle=rotation))
                else:
                    self.bottle_list.append(self.new_bottle(x + shift_x, y + shift_y, angle=rotation, broken=False))

    def new_bottle(self, x, y, angle=0, broken=False):
        if broken:
            bottle = arcade.Sprite("assets/bottle0.png", scale=0.25)
        else:
            bottle = arcade.Sprite("assets/bottle1.png", scale=0.25)
        bottle.center_x = x
        bottle.center_y = y
        bottle.angle = angle
        return bottle

    def new_broken_bottle(self, bottle):
        broken_bottle = self.new_bottle(bottle.center_x, bottle.center_y, angle=bottle.angle, broken=True)
        return broken_bottle

    def draw_crosshair(self):
        x, y = self.mouse_pos
        pad = 3
        arcade.draw_line(x - 10, y, x - pad, y, arcade.color.RED, 2)
        arcade.draw_line(x + 10, y, x + pad, y, arcade.color.RED, 2)
        arcade.draw_line(x, y - 10, x, y - pad, arcade.color.RED, 2)
        arcade.draw_line(x, y + 10, x, y + pad, arcade.color.RED, 2)

    def on_draw(self):
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, (92, 64, 51))
        self.bottle_list.draw()
        self.broken_bottle_list.draw()
        self.draw_crosshair()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_pos = (x, y)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            hit = arcade.get_sprites_at_point((x, y), self.bottle_list)
            if hit:
                arcade.play_sound(self.bottle_sound, 0.1)
            for b in hit:
                self.bottle_list.remove(b)
                self.broken_bottle_list.append(self.new_broken_bottle(b))
            if not self.bottle_list:
                self.window.show_win_view()


class WinView(arcade.View):
    def __init__(self, window: arcade.Window = None):
        super().__init__(window)

    def setup(self):
        pass

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("ETO POBEDA", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
            arcade.color.WHITE, font_name='Kenney High Square', font_size=50, anchor_x="center")

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.window.show_game_view()


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
        self.win_view = WinView(self)

    def setup(self):
        self.show_splash_view()

    def show_game_view(self):
        self.game_view.setup()
        self.show_view(self.game_view)

    def show_splash_view(self):
        self.splash_view.setup()
        self.show_view(self.splash_view)

    def show_win_view(self):
        self.win_view.setup()
        self.show_view(self.win_view)


def main():
    arcade.enable_timings()
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
