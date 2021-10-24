import pyglet as pg
import os
from pyglet.window import key

pg.resource.path = ['./img']
pg.resource.reindex()

img_list = list(os.walk('./img'))[0][2]
#print(img_list)
for i in img_list:
    if i[i.rfind('.') + 1:] in ['psd', 'zip', 'txt']:
        img_list.pop(img_list.index(i))

img = {i[:i.rfind('.')]: pg.resource.image(i) for i in img_list}

pg.resource.path = ['./img/not\'s']
pg.resource.reindex()
song = list(os.walk('./img/not\'s'))[0][2]
#print(song)
for i in song:
    if i[i.rfind('.') + 1:] not in ['mp3']:
        song.pop(song.index(i))

song = {i[i[:i.rfind('.')].rfind('.') + 1:i.rfind('.')]: pg.resource.media(i) for i in song}
#print(*[i + '\n' for i in song.keys()])


class Nota:
    class_Nota = {
        'w1': [img['left'], img['left_pushed']],
        'w2': [img['midle'], img['midle_pushed']],
        'w3': [img['right'], img['right_pushed']],
        'b1': [img['black'], img['black_pushed']]
    }
    name_ql = {
        'EQUAL' : '=',
        'BRACKETLEFT': '[',
        'BRACKETRIGHT' : ']'
    }

    def __init__(self, sound, class_nota, but, x, y):
        if but in self.name_ql:
            self.but = self.name_ql[but]
        else:
            self.but = but

        self.class_nota = class_nota
        self.sprite = [pg.sprite.Sprite(i) for i in self.class_Nota[class_nota]]
        for i in range(len(self.sprite)):
            self.sprite[i].x = x
            self.sprite[i].y = y

        if class_nota != 'b1':
            self.label = pg.text.Label(self.but, font_name='Calibri',
                                   font_size=8*scale_x, x=x+2.5*scale_x+margin,
                                   y=12*scale_y,color=[255, 0, 0, 255])
        else:
            self.label = pg.text.Label(self.but[-1], font_name='Calibri',
                                       font_size=8 * scale_x, x=x + 5 * scale_x+margin,
                                       y= self.sprite[0].height * (1-54/82) + 15 * scale_y, color=[255, 0, 0, 255])

        self.sound = song[sound]
        self.push = 0
        self.player = pg.media.Player()
        self.player.queue(self.sound)

    def scale(self, scale_x=1, scale_y=1):
        self.sprite[0].scale_x = scale_x
        self.sprite[0].scale_y = scale_y
        self.sprite[1].scale_x = scale_x
        self.sprite[1].scale_y = scale_y

        if self.class_nota == 'b1':
            self.target_x = [self.sprite[0].x, self.sprite[0].x + self.sprite[0].width]
            self.target_y = [self.sprite[0].height * (1-54/82), self.sprite[0].height]
        else:
            self.target_x = [self.sprite[0].x, self.sprite[0].x + self.sprite[0].width]
            self.target_y = [0, self.sprite[0].height]

    def target(self, x, y):
        return self.target_x[0] <= x < self.target_x[1] and self.target_y[0] <= y < self.target_y[1]

    def play(self):
        self.player.queue(self.sound)
        self.player.play()
        self.push = 1

    def stop(self):
        self.player.pause()
        self.player.next_source()
        self.player.pause()
        self.player.next_source()
        self.player.pause()
        self.push = 0


count_white = 12
count_black = 8

button = {}
margin = 3

#Маштаб нот
scale_x = 2
scale_y = 1.5

with open('setting.txt') as f:
    for i in range(count_white):
        arri = f.readline().split()
        button[arri[2]] = Nota(*arri, scale_x * i * (img['left'].width) + margin, 0)
    for i in range(count_black):
        arri = f.readline().split()
        if arri[2] not in ['EQUAL','_0']:
            j = int(arri[2][-1])-2
            button[arri[2]] = Nota(*arri, x=margin + scale_x * ((j + 1) * img['left'].width - img['black'].width / 2),
                                   y=scale_y *(img['left'].height - img['black'].height))
        elif arri[2] == '_0':
            button[arri[2]] = Nota(*arri, x=margin + scale_x * (9 * img['left'].width - img['black'].width / 2),
                                   y=scale_y *(img['left'].height - img['black'].height))
        else:
            button[arri[2]] = Nota(*arri, x=margin + scale_x * (11 * img['left'].width - img['black'].width / 2),
                                   y=scale_y *(img['left'].height - img['black'].height))

#Маштабирование
for i in button:
    button[i].scale(scale_x, scale_y)

win = pg.window.Window(width=int(img['left'].width * count_white*scale_x+margin*2),
                       height=int(img['left'].height*scale_y))

fps = pg.window.FPSDisplay(win)
keyboard = key.KeyStateHandler()
win.push_handlers(keyboard)

'''
event_logger = pg.window.event.WindowEventLogger()  # Показывает все зарегестрированые события
win.push_handlers(event_logger)
'''

@win.event
def on_draw():
    win.clear()
    fps.draw()
    for i in button.values():
        i.sprite[i.push].draw()
        i.label.draw()


@win.event
def on_key_press(symbol, modifiers):
    win.push_handlers(keyboard)
    for key1, val in keyboard.items():
        #if key1 == key.T:
            #print(keyboard)
        if val and key.symbol_string(key1) in button:
            if key.symbol_string(key1) and button[key.symbol_string(key1)].push == 0:
                button[key.symbol_string(key1)].play()
        elif val and key1 in [949187772416, 940597837824]:
            if key1 == 940597837824:
                k = 91
            else:
                k = 93
            if button[key.symbol_string(k)].push == 0:
                button[key.symbol_string(k)].play()


@win.event
def on_key_release(symbol, modifiers):
    win.push_handlers(keyboard)
    for key1, val in keyboard.items():
        if not val and key.symbol_string(key1) in button:
            if key.symbol_string(key1) and button[key.symbol_string(key1)].push == 1:
                button[key.symbol_string(key1)].stop()
        elif not val and key1 in [949187772416, 940597837824]:
            if key1 == 940597837824:
                k = 91
            else:
                k = 93
            if button[key.symbol_string(k)].push == 1:
                button[key.symbol_string(k)].stop()

@win.event
def on_mouse_press(x, y, but, modifiers):
    global last_mouse_button
    for i in list(button.keys())[::-1]:
        if button[i].target(x, y) and button[i].push == 0:
            button[i].play()
            last_mouse_button = button[i]
            break

@win.event
def on_mouse_release(x, y, but, modifiers):
    for i in list(button.keys())[::-1]:
        if button[i].target(x, y) and button[i].push == 1:
            button[i].stop()
            break

@win.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global last_mouse_button
    f = 0
    for i in list(button.keys())[:-9:-1]:
        f += button[i].target(x, y) and button[i].push == 0
    if not last_mouse_button.target(x,y) or f:
        last_mouse_button.stop()
        for i in list(button.keys())[::-1]:
            if button[i].target(x, y) and button[i].push == 0:
                button[i].play()
                last_mouse_button = button[i]
                break

pg.app.run()
