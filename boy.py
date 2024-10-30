from pico2d import load_image, get_time

from state_machine import StateMachine, space_down, time_out, right_down, right_up, left_down, left_up, auto_run


class Idle:
    @staticmethod
    def enter(boy, e):
        if left_up(e) or right_down(e):
            boy.action = 2
        elif right_up(e) or left_down(e):
            boy.action = 3

        boy.dir = 0
        boy.frame = 0
        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.action == 3:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, 3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        elif boy.action == 2:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.dir = 1
            boy.action = 1
        elif left_down(e) or right_up(e):
            boy.dir = -1
            boy.action = 0

        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class AutoRun:
    @staticmethod
    def enter(boy, e):
        if boy.action == 3:
            boy.dir = 1
            boy.action = 1
        elif boy.action == 2:
            boy.dir = -1
            boy.action = 0

        boy.frame = 0
        boy.s = 0
        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        boy.s += 1
        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y + boy.s // 4, 100 + boy.s, 100 + boy.s)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, auto_run : AutoRun},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, auto_run : AutoRun},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle, auto_run : AutoRun},
                AutoRun: {time_out: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event( ('INPUT', event) )

    def draw(self):
        self.state_machine.draw()

