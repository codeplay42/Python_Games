'''
项目：Flappy Bird

操作说明：
    1.按 S 键开始游戏/重新开始游戏
    2.按空格控制小鸟飞跃
'''

import arcade
from random import randint

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game_state = 'start'
        self.score = 0
        self.bg = arcade.Sprite('images/bg.png')  # 导入角色
        self.bg.left = 0
        self.bg.top = 600
        self.ground = arcade.Sprite('images/ground.png')
        self.ground.left = 0
        self.ground.top = 96
        self.count = 0
        self.bird_list = arcade.SpriteList()  # 创建存放小鸟不同造型的列表
        self.bird_change_y = 5
        for i in range(4):
            self.bird_list.append(arcade.Sprite(
                'images/bird{}.png'.format(i), center_x=150, center_y=300))
        self.pipe_up = arcade.Sprite('images/pipe_up.png')
        self.pipe_up.left = 500
        self.pipe_up.bottom = 400
        self.pipe_down = arcade.Sprite('images/pipe_down.png')
        self.pipe_down.left = self.pipe_up.left
        self.pipe_down.top = self.pipe_up.bottom - 120
        self.cover = arcade.Sprite(
            'images/cover.png', center_x=225, center_y=300)
        self.game_over = arcade.Sprite(
            'images/game_over.png', center_x=225, center_y=400)
        self.sound_coin = arcade.load_sound('audio/point.ogg')  # 导入声音
        self.sound_die = arcade.load_sound('audio/die.ogg')

    def on_draw(self):
        arcade.start_render()
        if self.game_state == 'start':
            self.cover.draw()  # 显示开始画面
        else:
            self.bg.draw()
            self.pipe_up.draw()
            self.pipe_down.draw()
            self.ground.draw()
            self.bird_animate()
            arcade.draw_text('score: ' + str(self.score), 10,
                             560, (255, 255, 255), font_size=20)
            if self.game_state == 'game over':
                self.game_over.draw()

    def on_update(self, delta_time):
        if self.game_state == 'playing':
            # 设置不同造型小鸟的坐标
            self.bird_list[0].center_y -= self.bird_change_y
            self.bird_change_y += 0.3
            for i in range(1, 4):
                self.bird_list[i].center_y = self.bird_list[0].center_y
            self.pipe_up.center_x -= 3
            self.pipe_down.center_x = self.pipe_up.center_x  # 下管道和上管道的 x 坐标相同
            self.ground.center_x -= 3
            # 管道移出屏幕，重置位置到屏幕右方
            if self.pipe_up.center_x < -100:
                self.pipe_up.left = randint(500, 600)
                self.pipe_up.bottom = randint(360, 480)
                self.pipe_down.top = self.pipe_up.bottom - 120
            # 检测管道与小鸟的碰撞
            if arcade.check_for_collision_with_list(self.pipe_up, self.bird_list) or \
                    arcade.check_for_collision_with_list(self.pipe_down, self.bird_list):
                self.game_state = 'game over'
                arcade.play_sound(self.sound_die)
            if self.ground.right < 500:
                self.ground.left = 0
            # 计算得分：管道右侧坐标小于小鸟左侧坐标时，得分 +1
            if self.pipe_up.right >= self.bird_list[0].left - 3 and self.pipe_up.right < self.bird_list[0].left:
                self.score += 1
                arcade.play_sound(self.sound_coin)

    def on_key_press(self, key, modifiers):
        # 按 S 键开始游戏/重新开始游戏
        if key == arcade.key.S:
            self.game_state = 'playing'
            self.score = 0
            for i in range(4):
                self.bird_list[i].center_x, self.bird_list[
                    i].center_y = 150, 300
            self.pipe_up.left, self.pipe_up.bottom = 500, 400
            self.pipe_down.left, self.pipe_down.top = 500, 280
        # 按空格键小鸟飞跃
        if key == arcade.key.SPACE:
            if self.game_state == 'playing':
                self.bird_change_y = -6

    # 小鸟飞翔动画，用 self.count 控制动画速度
    def bird_animate(self):
        self.bird_list[int(self.count / 4)].draw()
        if self.game_state == 'playing':
            self.count += 1
        if self.count > 15:
            self.count = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'Flappy Bird')
    arcade.run()

if __name__ == '__main__':
    main()
