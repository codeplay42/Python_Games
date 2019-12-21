# 操作说明：按空格键重新开始游戏，
'''
项目：Pipeline Mario

操作说明：
    1.按 A 键开始游戏/重新开始游戏
    2.上键跳跃，左右键左右移动，X 键发射火球

注意：
    1.每接到一个金币，就可以发生一个火球
    2.游戏屏幕尺寸较大，如果无法完整显示游戏，请调整电脑屏幕缩放比例
'''

import arcade
from random import randint

SCREEN_WIDTH = 1290
SCREEN_HEIGHT = 1010
SCREEN_TITLE = 'Pipeline Mario'

# 设置物理引擎参数
MOVE_SPEED = 6
JUMP_SPEED = 15
GRAVITY = 0.5


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game_state = 'start'
        self.score = 0
        self.coin_sound = arcade.load_sound('sounds/coin.wav')
        self.jump_sound = arcade.load_sound('sounds/jump.wav')
        # 导入封面、game over、马里奥 icon、金币 icon、地板
        self.cover = arcade.Sprite(
            'images/cover.png', center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
        self.game_over = arcade.Sprite(
            'images/game_over.png', center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2 + 100)
        self.mario_icon = arcade.Sprite(
            'images/mario_icon.png', center_x=SCREEN_WIDTH / 2 - 100, center_y=SCREEN_HEIGHT - 50)
        self.coin_icon = arcade.Sprite(
            'images/coin_icon.png', center_x=SCREEN_WIDTH / 2 + 100, center_y=SCREEN_HEIGHT - 50)
        self.floor = arcade.Sprite(
            'images/floor.png', center_x=SCREEN_WIDTH / 2, center_y=40)
        self.mario_list = arcade.SpriteList()
        for i in range(8):
            self.mario_list.append(arcade.Sprite(
                'images/mario{}.png'.format(i + 1), center_x=100, center_y=136))
        self.mario = arcade.Sprite(
            'images/mario1.png', center_x=100, center_y=136)
        self.direction = 0
        self.index = 0
        self.count = False
        self.timer = 0
        self.key_pressed = False
        self.pipe_up = arcade.SpriteList()
        self.pipe_down = arcade.SpriteList()
        self.bricks = arcade.SpriteList()
        self.bricks.append(self.floor)
        self.monsters = arcade.SpriteList()
        pipe_up_pos = [(120, SCREEN_HEIGHT - 180),
                       (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 180)]
        pipe_down_pos = [(80, 145), (SCREEN_WIDTH - 80, 145)]
        # 导入火球、金币、敌人角色
        self.fireball = arcade.Sprite(
            'images/fireball1.png', center_x=-100, center_y=100)
        self.shoot = False
        self.coin_list = arcade.SpriteList()
        self.enermy_list = arcade.SpriteList()
        # 导入水管角色
        for i in range(2):
            pipe_up = arcade.Sprite('images/pipe_up{}.png'.format(i + 1),
                                    center_x=pipe_up_pos[i][0], center_y=pipe_up_pos[i][1])
            pipe_down = arcade.Sprite('images/pipe_down{}.png'.format(
                i + 1), center_x=pipe_down_pos[i][0], center_y=pipe_down_pos[i][1])
            coin = arcade.Sprite(
                'images/coin.png', center_x=250 + 790 * i, center_y=SCREEN_HEIGHT - 155)
            turtle = arcade.Sprite(
                'images/turtle{}.png'.format(i + 1), center_x=250 + 790 * i, center_y=SCREEN_HEIGHT - 155)
            self.pipe_up.append(pipe_up)
            self.pipe_down.append(pipe_down)
            self.coin_list.append(coin)
            self.enermy_list.append(turtle)
        # 绘制砖块
        num_list = [16, 16, 16, 6, 6, 14, 14]
        birck_pos = [(-60, SCREEN_HEIGHT - 290), (SCREEN_WIDTH - num_list[1] * 40 + 100, SCREEN_HEIGHT - 290),
                     (SCREEN_WIDTH / 2 - num_list[2]
                      * 20 + 20, SCREEN_HEIGHT - 500),
                     (-60, SCREEN_HEIGHT - 550), (SCREEN_WIDTH -
                                                  num_list[4] * 40 + 100, SCREEN_HEIGHT - 550),
                     (-60, SCREEN_HEIGHT - 750), (SCREEN_WIDTH - num_list[6] * 40 + 100, SCREEN_HEIGHT - 750)]

        for i in range(7):
            for j in range(num_list[i]):
                brick = arcade.Sprite('images/brick.png')
                brick.center_x = birck_pos[i][0] + j * 40
                brick.center_y = birck_pos[i][1]
                self.bricks.append(brick)

        self.life = 3
        self.coin_num = 0  # 收集金币数量
        self.fireball_num = 0  # 火球数量，每收集一个金币，可以发射一个火球
        self.fireball_speed = MOVE_SPEED

        # 给马里奥、乌龟、金币添加物理引擎
        pe_list = [self.mario, self.coin_list[0], self.coin_list[
            1], self.enermy_list[0], self.enermy_list[1]]
        self.physics_engine = []
        for sprite in pe_list:
            self.physics_engine.append(arcade.PhysicsEnginePlatformer(
                sprite, self.bricks, gravity_constant=GRAVITY))

    def on_draw(self):
        arcade.start_render()
        if self.game_state == 'start':
            self.cover.draw()
        else:
            # 显示角色
            self.enermy_list.draw()
            self.coin_list.draw()
            self.pipe_up.draw()
            self.pipe_down.draw()
            self.mario_list[self.index].draw()
            self.bricks.draw()
            self.fireball.draw()
            self.mario_icon.draw()
            self.coin_icon.draw()
            arcade.draw_text('x {}'.format(self.life), SCREEN_WIDTH /
                             2 - 70, SCREEN_HEIGHT - 65, (255, 255, 255), font_size=30)
            arcade.draw_text('x {}'.format(self.coin_num), SCREEN_WIDTH /
                             2 + 122, SCREEN_HEIGHT - 65, (255, 255, 255), font_size=30)
            if self.game_state == 'game over':
                self.game_over.draw()

    def on_update(self, delta_time):
        if self.game_state == 'playing':
            # 限制马里奥的 x 坐标范围
            self.set_boundary(self.mario, 40)
            # 乌龟与金币移动
            for i in range(len(self.enermy_list)):
                self.enermy_list[i].change_x = 4 - i * 8
                self.coin_list[i].change_x = 3 - i * 6
                self.set_boundary(self.enermy_list[i], 40)
                self.set_boundary(self.coin_list[i], 20)
                if self.enermy_list[i].center_y < 150 and abs(self.enermy_list[i].center_x - SCREEN_WIDTH * (1 - i)) < 120:
                    self.reset_pos(self.enermy_list[i], i)
                if self.coin_list[i].center_y < 150 and abs(self.coin_list[i].center_x - SCREEN_WIDTH * (1 - i)) < 140:
                    self.reset_pos(self.coin_list[i], i)
            # 发射火球
            if self.shoot:
                if self.fireball.center_x > -100 and self.fireball.center_x < SCREEN_WIDTH + 100:
                    self.fireball.center_x += self.fireball_speed
                else:
                    self.shoot = False

            # 碰撞检测
            for i in range(len(self.enermy_list)):
                if arcade.check_for_collision(self.mario, self.enermy_list[i]):
                    self.life -= 1
                    self.reset_pos(self.enermy_list[i], i)
                    if self.life == 0:
                        self.game_state = 'game over'
                if arcade.check_for_collision(self.mario, self.coin_list[i]):
                    self.coin_num += 1
                    self.fireball_num += 1
                    self.score += 1
                    arcade.play_sound(self.coin_sound)
                    self.reset_pos(self.coin_list[i], i)
                if arcade.check_for_collision(self.fireball, self.enermy_list[i]):
                    self.score += 1
                    self.reset_pos(self.enermy_list[i], i)
            # 马里奥移动时才切换造型，形成跑动的动画
            if self.count:
                if self.direction == 0:
                    self.timer += 1
                    if self.timer > 600:
                        self.timer = 0
                    if self.timer % 2 == 0:
                        self.index += 1
                        if self.index > 3:
                            self.index = 0
                else:
                    self.timer += 1
                    if self.timer % 2 == 0:
                        self.index += 1
                        if self.index > 7:
                            self.index = 4
            self.mario_list[self.index].center_x = self.mario.center_x
            self.mario_list[self.index].center_y = self.mario.center_y
            if self.key_pressed and self.physics_engine[0].can_jump():
                self.count = True
            else:
                self.count = False

            # update 物理引擎
            for pe in self.physics_engine:
                pe.update()

    def set_boundary(self, obj, dis):  # 角色移出屏幕后，从屏幕另一侧出现
        if obj.center_x < -dis:
            obj.center_x = SCREEN_WIDTH + dis
        elif obj.center_x > SCREEN_WIDTH + dis:
            obj.center_x = -dis

    def reset_pos(self, obj, index):  # 重置角色的位置到上面的水管出口处
        obj.center_x = 250 + 790 * index
        obj.center_y = SCREEN_HEIGHT - 155

    def on_key_press(self, key, modifiers):
        # A 键开始游戏
        if key == arcade.key.A:
            self.game_state = 'playing'
        # 上键跳跃，左右键左右移动，X 键发射火球
        if key == arcade.key.UP:
            if self.physics_engine[0].can_jump():
                self.mario.change_y = JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        if key == arcade.key.LEFT:
            self.mario.change_x = -MOVE_SPEED
            self.key_pressed = True
            self.direction = 0
            if self.index > 3:
                self.index -= 4
        elif key == arcade.key.RIGHT:
            self.mario.change_x = MOVE_SPEED
            self.key_pressed = True
            self.direction = 1
            if self.index < 4:
                self.index += 4
        if key == arcade.key.X:
            if self.fireball_num > 0:
                self.shoot = True
                self.fireball_num -= 1
                # 将火球移到马里奥附近
                self.fireball.center_x = self.mario.center_x
                self.fireball.center_y = self.mario.center_y
                if self.direction == 1:
                    self.fireball_speed = MOVE_SPEED
                else:
                    self.fireball_speed = -MOVE_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.mario.change_x = 0
            self.key_pressed = False


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == '__main__':
    main()
