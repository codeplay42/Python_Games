'''
项目：球动画
描述：球按照正弦关系上下移动的动画
'''

import arcade
import math


class Ball:

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255, 191, 0)


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color((10, 186, 181))
        self.t = 0
        self.ball_list = []  # 创建球列表
        for i in range(6):
            ball = Ball(200 + 80 * i, 100, 20)
            self.ball_list.append(ball)

    def on_draw(self):
        arcade.start_render()
        for ball in self.ball_list:  # for循环画球
            arcade.draw_circle_filled(ball.x, ball.y, ball.size, ball.color)

    def on_update(self, delta_time):
        # for循环更新球的坐标，相邻球相位差30度
        for i in range(len(self.ball_list)):
            self.ball_list[i].y = 300 + 100 * \
                math.sin(math.radians(self.t + 30 * i))
        self.t += 4


def main():
    game = MyGame(800, 600, 'First Game')
    arcade.run()

if __name__ == '__main__':
    main()
