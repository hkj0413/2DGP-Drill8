from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_a

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def auto_run(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []

    def start(self, start_state):
        self.cur_state = start_state
        self.cur_state.enter(self.o, ('START', 0))

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            e = self.event_que.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    self.cur_state.exit(self.o, e)
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                    return

    def draw(self):
        self.cur_state.draw(self.o)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def add_event(self, e):
        self.event_que.append(e)