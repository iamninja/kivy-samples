from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
  score = NumericProperty(0)

  def bounce_ball(self, ball):
    if self.collide_widget(ball):
      vx, vy = ball.velocity
      offset = (ball.center_y - self.center_y) / (self.height / 2)
      bounced = Vector(-1 * vx, vy)
      vel = bounced * 1.1
      ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):

  # Velocity for the ball
  velocity_x = NumericProperty(0)
  velocity_y = NumericProperty(0)

  # referencelist property (create shorthand)
  velocity = ReferenceListProperty(velocity_x, velocity_y)

  # the "move" function

  def move(self):
    self.pos = Vector(*self.velocity) + self.pos



class PongGame(Widget):

  ball = ObjectProperty(None)
  player1 = ObjectProperty(None)
  player2 = ObjectProperty(None)

  def serve_ball(self, vel=(4,0)):
    # Start the ball to a random direction
    self.ball.center = self.center
    self.ball.velocity = vel

  def update(self, dt):
    # Update function
    self.ball.move()

    # bounce on paddles
    self.player1.bounce_ball(self.ball)
    self.player2.bounce_ball(self.ball)

    # bounce between top and bottom
    if (self.ball.y < 0) or (self.ball.top > self.height):
      self.ball.velocity_y *= -1

    # score point and serve ball when touch left and right
    if (self.ball.x < self.x):
      self.player2.score += 1
      self.serve_ball(vel=(4, 0))
    if (self.ball.x > self.width):
      self.player1.score += 1
      self.serve_ball(vel=(-4, 0))

  def on_touch_move(self, touch):
    if touch.x < self.width / 3:
      self.player1.center_y = touch.y
    if touch.x > self.width - self.width / 3:
      self.player2.center_y = touch.y



class PongApp(App):

  def build(self):
    game = PongGame()
    game.serve_ball()
    # Update game screen 60 times per second
    Clock.schedule_interval(game.update, 1.0/60.0)
    return game


if __name__ == '__main__':
  PongApp().run()
