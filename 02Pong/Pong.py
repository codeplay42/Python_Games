'''
项目：经典游戏 Pong

操作说明：
    1.用 W、S、上、下键分别控制左右平板上下移动
'''

import math
import arcade
from random import randint

# 设定游戏屏幕尺寸和名字
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Pong'
MOVE_SPEED = 10


class Ball:

    def __init__(self, x, y, change_x, change_y, radius):
        self.x = x
        self.y = y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = (255, 191, 0)

    def draw(self):
        # 画球
        arcade.draw_circle_filled(
            self.x, self.y, self.radius, self.color)

    def update(self):
        # 球移动
        self.x += self.change_x
        self.y += self.change_y
        # 碰到边缘反弹
        if self.x < self.radius + 5 or self.x > SCREEN_WIDTH - self.radius - 5:
            self.change_x *= -1
        if self.y < self.radius or self.y > SCREEN_HEIGHT - self.radius:
            self.change_y *= -1


class Rect:  # 平板

    def __init__(self, x, y, change_y, width, height):
        self.x = x
        self.y = y
        self.change_y = change_y
        self.width = width
        self.height = height
        self.color = (175, 0, 42)

    def draw(self):
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height, self.color)

    def update(self):
        self.y += self.change_y


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color((10, 186, 181))
        self.ball = Ball(200, 500, 8, 8, 20)
        self.rect_list = [Rect(5, 300, 0, 10, 100),
                          Rect(795, 300, 0, 10, 100)]
        self.score_list = [0, 0]
        self.bounce_sound = arcade.load_sound('bounce.wav')  # 导入声音

    def on_draw(self):  # 绘制角色
        arcade.start_render()
        self.ball.draw()
        for i in range(len(self.rect_list)):
            self.rect_list[i].draw()
            arcade.draw_text(
                'score: ' + str(self.score_list[i]), 30 + i * 620, 560, (175, 0, 42), font_size=26)

    def on_update(self, delta_time):
        self.ball.update()
        for rect in self.rect_list:
            rect.update()
        self.collision_detect()

    def collision_detect(self):
        # 碰撞检测
        for i in range(len(self.rect_list)):
            dis = abs(self.ball.x - self.rect_list[i].x)
            if dis <= self.ball.radius + self.rect_list[i].width / 2:
                if abs(self.ball.y - self.rect_list[i].y) < self.rect_list[i].height / 2:
                    self.score_list[i] += 1
                    arcade.play_sound(self.bounce_sound)

    def on_key_press(self, key, modifiers):
        # 用W、S、上、下按键控制左右平板上下移动
        if key == arcade.key.UP:
            self.rect_list[1].change_y = MOVE_SPEED
        elif key == arcade.key.DOWN:
            self.rect_list[1].change_y = -MOVE_SPEED
        if key == arcade.key.W:
            self.rect_list[0].change_y = MOVE_SPEED
        elif key == arcade.key.S:
            self.rect_list[0].change_y = -MOVE_SPEED

    def on_key_release(self, key, modifiers):
        # 按键松开时，平板不移动
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.rect_list[1].change_y = 0
        if key == arcade.key.W or key == arcade.key.S:
            self.rect_list[0].change_y = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == '__main__':
    main()
