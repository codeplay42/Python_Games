'''
项目：Ninja Adventure

操作说明：
    1.上键跳跃，左右键移动
    2.A键发射飞镖
    3.按空格键重新开始游戏
'''

import arcade
from random import randint

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 688
SCREEN_TITLE = 'Ninja Adventure'


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game_state = 'playing'
        self.score = 0
        self.bg = arcade.Sprite('images/bg.png')  # 导入背景
        self.bg.left = 0
        self.bg.top = 688
        self.ninja = arcade.Sprite('images/ninja.png')
        self.ninja.left = 100
        self.ninja.bottom = 110
        self.dart = arcade.Sprite(
            'images/dart.png', center_x=-100, center_y=300)
        self.jump = False
        self.jump_speed = 12
        self.shoot = False
        self.monster_list = arcade.SpriteList()  # 创建怪物角色列表
        for i in range(3):
            self.monster_list.append(arcade.Sprite(
                'images/ghost1.png', center_x=1280 + 400 * i, center_y=150))
        self.life = 3
        self.level = 1

    def on_draw(self):
        arcade.start_render()
        if self.game_state == 'start':
            self.bg.draw()  # 显示开始画面
        else:
            self.bg.draw()
            self.ninja.draw()
            self.dart.draw()
            self.monster_list.draw()
            arcade.draw_text('score: ' + str(self.score), 1020,
                             620, (255, 255, 255), font_size=30)
            arcade.draw_text('level: ' + str(self.level), 900,
                             620, (255, 255, 255), font_size=30)
            arcade.draw_text('life: ' + str(self.life), 780,
                             620, (255, 255, 255), font_size=30)
            if self.game_state == 'game over':
                arcade.draw_text('Game Over', 500,
                                 400, (229, 43, 80), font_size=50)
            if self.game_state == 'You Win':
                arcade.draw_text('You Win', 500,
                                 400, (255, 255, 255), font_size=50)

    def on_update(self, delta_time):
        if self.game_state == 'playing':
            # 怪物移动
            for monster in self.monster_list:
                monster.center_x -= 3 + self.level
                if monster.center_x < -100:
                    self.reset_monster(monster)
            # 忍者移动和跳跃
            self.ninja.center_x += self.ninja.change_x
            if self.jump:
                self.ninja.bottom += self.jump_speed
                self.jump_speed -= 0.3
                if self.ninja.bottom < 110:
                    self.jump = False
                    self.jump_speed = 12
            # 飞镖移动
            if self.shoot:
                if self.dart.center_x < SCREEN_WIDTH + 20 and self.dart.center_x > -20:
                    self.dart.center_x += 8
                else:
                    self.shoot = False
            # 碰撞检测
            for i in range(len(self.monster_list)):
                if arcade.check_for_collision(self.ninja, self.monster_list[i]):
                    self.life -= 1
                    self.reset_monster(self.monster_list[i])
                    if self.life == 0:
                        self.game_state = 'game over'
                if arcade.check_for_collision(self.dart, self.monster_list[i]):
                    self.score += 1
                    self.reset_monster(self.monster_list[i])
                    self.dart.center_x = -100
                    if self.score > 50:
                        self.score = 0
                        self.level += 1
                        if self.level > 3:
                            self.game_state = 'You Win'

    def reset_monster(self, monster):
        monster.center_x = randint(1260, 1600)
        monster.center_y = randint(150, 240)

    def on_key_press(self, key, modifiers):
        # 按空格键忍者跳跃
        if self.game_state == 'playing':
            if key == arcade.key.UP:
                self.jump = True
            if key == arcade.key.LEFT:
                self.ninja.change_x = -4
            if key == arcade.key.RIGHT:
                self.ninja.change_x = 4
            # 按 A 键发射飞镖
            if key == arcade.key.A:
                self.shoot = True
                self.dart.center_x = self.ninja.center_x
                self.dart.center_y = self.ninja.center_y
        # 按空格键重新开始游戏
        if key == arcade.key.SPACE:
            self.game_state = 'playing'
            self.life = 3
            self.score = 0
            for i in range(len(self.monster_list)):
                self.monster_list[i].center_x = 1280 + 400 * i
            self.level = 1

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.ninja.change_x = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == '__main__':
    main()
