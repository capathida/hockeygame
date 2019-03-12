from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class HockeyStick(Widget):
    score = NumericProperty(0)

    def bounce_puck(self, puck):
        if self.collide_widget(puck):
            vx, vy = puck.velocity
            offset = (puck.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            puck.velocity = vel.x, vel.y + offset


class Puck(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class HockeyGame(Widget):
    puck = ObjectProperty(None)
    player = ObjectProperty(None)
    timer = ObjectProperty(None)

    def start_puck(self, vel=(4, 0)):
        self.puck.center = self.center
        self.puck.velocity = vel

    def update(self, dt):
        self.puck.move()

        # bounce of stick
        self.player.bounce_puck(self.puck)

        # bounce puck off bottom or top
        if (self.puck.y < self.y) or (self.puck.top > self.top):
            self.puck.velocity_y *= -1

        # went of to a side to score point?
        if self.puck.x < self.x:
            self.player.score += 1
            self.start_puck(vel=(4, 0))

        if self.puck.x > self.width:
            self.puck.velocity_y *= -1

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player.center_y = touch.y


class HockeyApp(App):
    def build(self):
        game = HockeyGame()
        game.start_puck()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    HockeyApp().run()