'''
项目：Bongo Cat
参考此项目制作(https://github.com/Externalizable/bongo.cat)

操作说明：
    1.按 A、S、D 打鼓
    2.按 0-8 弹琴
    3.按空格 meow

弹奏 Demo：
Happy Birthday to You
1 1 3 1 6 5
1 1 3 1 8 6

Ode to Joy - Friedrich Schiller
5 5 6 8 8 6 5 3 1 1 3 5 5 3 3
5 5 6 8 8 6 5 3 1 1 3 5 3 1 1
3 3 5 1 3 5 6 5 1 3 5 6 5 3 1 3 1

In the End - Linkin Park
3 0 0 6 5 5 5 5 6 3
0 0 6 5 5 5 5 6 3
'''

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color((255, 255, 255))
        self.instrument_list = arcade.SpriteList()  # 乐器角色列表
        self.bongo = arcade.Sprite(
            'images/bongo.png', center_x=400, center_y=225)
        self.keyboard = arcade.Sprite(
            'images/keyboard.png', center_x=400, center_y=225)
        self.instrument_list.append(self.bongo)
        self.instrument_list.append(self.keyboard)
        self.instrument_index = 0  # 用于切换乐器
        # 导入嘴巴、爪子角色
        self.mouth_list = arcade.SpriteList()
        self.hand_l_list = arcade.SpriteList()
        self.hand_r_list = arcade.SpriteList()
        for i in range(2):
            self.mouth_list.append(arcade.Sprite(
                'images/m{}.png'.format(i + 1), center_x=400, center_y=225))
            self.hand_l_list.append(arcade.Sprite(
                'images/l{}.png'.format(i + 1), center_x=400, center_y=225))
            self.hand_r_list.append(arcade.Sprite(
                'images/r{}.png'.format(i + 1), center_x=400, center_y=225))
        self.mouth_index = 0
        self.hand_index = [0, 0]
        # 导入声音
        self.bongo_sound = []
        for i in range(2):
            self.bongo_sound.append(arcade.load_sound(
                'sounds/bongo{}.wav'.format(i)))
        self.keyboard_sound = []
        for i in range(10):
            self.keyboard_sound.append(arcade.load_sound(
                'sounds/keyboard{}.wav'.format(i)))
        self.meow_sound = arcade.load_sound('sounds/meow.wav')

    def on_draw(self):
        arcade.start_render()
        # 根据索引显示角色列表中的角色，索引由按键控制
        self.instrument_list[self.instrument_index].draw()
        self.mouth_list[self.mouth_index].draw()
        self.hand_l_list[self.hand_index[0]].draw()
        self.hand_r_list[self.hand_index[1]].draw()

    def on_key_press(self, key, modifiers):
        # 按 A、S、D 打鼓
        if key == arcade.key.A:
            self.instrument_index = 0
            self.hand_index[1] = 1
            arcade.play_sound(self.bongo_sound[1])
        if key == arcade.key.D:
            self.instrument_index = 0
            self.hand_index[0] = 1
            arcade.play_sound(self.bongo_sound[0])
        if key == arcade.key.S:
            self.instrument_index = 0
            self.hand_index[0] = 1
            self.hand_index[1] = 1
            arcade.play_sound(self.bongo_sound[0])
            arcade.play_sound(self.bongo_sound[1])
        # 按空格 meow
        if key == arcade.key.SPACE:
            self.mouth_index = 1
            arcade.play_sound(self.meow_sound)
        # 按 0-8 弹琴
        if key == arcade.key.KEY_0:
            self.instrument_index = 1
            self.hand_index[1] = 1
            arcade.play_sound(self.keyboard_sound[0])
        if key == arcade.key.KEY_1:
            self.instrument_index = 1
            self.hand_index[0] = 1
            arcade.play_sound(self.keyboard_sound[1])
        if key == arcade.key.KEY_2:
            self.instrument_index = 1
            self.hand_index[0] = 1
            arcade.play_sound(self.keyboard_sound[2])
        if key == arcade.key.KEY_3:
            self.instrument_index = 1
            self.hand_index[0] = 1
            arcade.play_sound(self.keyboard_sound[3])
        if key == arcade.key.KEY_4:
            self.instrument_index = 1
            self.hand_index[0] = 1
            arcade.play_sound(self.keyboard_sound[4])
        if key == arcade.key.KEY_5:
            self.instrument_index = 1
            self.hand_index[1] = 1
            arcade.play_sound(self.keyboard_sound[5])
        if key == arcade.key.KEY_6:
            self.instrument_index = 1
            self.hand_index[1] = 1
            arcade.play_sound(self.keyboard_sound[6])
        if key == arcade.key.KEY_7:
            self.instrument_index = 1
            self.hand_index[1] = 1
            arcade.play_sound(self.keyboard_sound[7])
        if key == arcade.key.KEY_8:
            self.instrument_index = 1
            self.hand_index[1] = 1
            arcade.play_sound(self.keyboard_sound[8])

    def on_key_release(self, key, key_modifiers):
        # 松开按键恢复到默认造型
        if key == arcade.key.A:
            self.hand_index[1] = 0
        if key == arcade.key.D:
            self.hand_index[0] = 0
        if key == arcade.key.S:
            self.hand_index[1] = 0
            self.hand_index[0] = 0
        if key == arcade.key.SPACE:
            self.mouth_index = 0
        if key == arcade.key.KEY_0:
            self.hand_index[1] = 0
        if key == arcade.key.KEY_1:
            self.hand_index[0] = 0
        if key == arcade.key.KEY_1:
            self.hand_index[0] = 0
        if key == arcade.key.KEY_2:
            self.hand_index[0] = 0
        if key == arcade.key.KEY_3:
            self.hand_index[0] = 0
        if key == arcade.key.KEY_4:
            self.hand_index[0] = 0
        if key == arcade.key.KEY_5:
            self.hand_index[1] = 0
        if key == arcade.key.KEY_6:
            self.hand_index[1] = 0
        if key == arcade.key.KEY_7:
            self.hand_index[1] = 0
        if key == arcade.key.KEY_8:
            self.hand_index[1] = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'Bongo Cat')
    arcade.run()

if __name__ == '__main__':
    main()
