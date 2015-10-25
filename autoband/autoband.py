# -*- coding: utf-8 -*-

import time

import pyglet
from pyglet.window import key


class Metronome(object):
    def __init__(self):
        self.last = None
        self.times = []
        self.average = None

    def tick(self, when):
        self.last = when
        self.times.append(when)
        while self.times and (when - self.times[0]) > 10:
            self.times.pop(0)
        if len(self.times) >= 4:
            self.average = self.average_tick_length()

    def average_tick_length(self):
        if len(self.times) < 2:
            return None
        return (self.times[-1] - self.times[0]) / (len(self.times) - 1)

    def next_tick(self, now):
        if self.average is None:
            return None
        return (self.last - now) % self.average


def main():
    window = pyglet.window.Window()

    label = pyglet.text.Label('Hello, world',
                              font_name='Times New Roman',
                              font_size=36,
                              x=window.width // 2,
                              y=window.height // 2,
                              anchor_x='center',
                              anchor_y='center')

    sound = pyglet.media.load('click.wav', streaming=False)

    metronome = Metronome()

    def tick(dt, do_play):
        if do_play:
            sound.play()
        next_tick = metronome.next_tick(time.time())
        pyglet.clock.schedule_once(tick, next_tick or .2,
                                   next_tick is not None)

    @window.event
    def on_draw():
        window.clear()
        label.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.A:
            metronome.tick(time.time())
            print 'The "A" key was pressed.'
        elif symbol == key.LEFT:
            print 'The left arrow key was pressed.'
        elif symbol == key.ENTER:
            print 'The enter key was pressed.'

    pyglet.clock.schedule_once(tick, .2, False)

    pyglet.app.run()


if __name__ == '__main__':
    main()
