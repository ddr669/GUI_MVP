import pygame as pg
#from pygame import font as FONT
import classBase

class Surface(pg.Surface):
    def __init__(self, size: tuple, bg_color: tuple = None):
        self.size = size
        self.bg_color = bg_color if bg_color else (25,25,25,25)
        super().__init__(size, pg.SRCALPHA)

class CascadeOption:
    def __init__(self, text: str = None, color: tuple = None, surf = None, pos: tuple = (0,0)):
        self.color = color if color else (25,25,25, 25)
        self.is_hover = False
        self.old_color = self.color
        self.text = text
        self.hover_color = (200,25,25, 25)
        self.surf = surf
        self.pos = pos
    

class Ball:
    def __init__(self,
            pos: tuple = None,
            color: tuple = None,
            *args,**kwargs):
        self.pos = pos
        if self.pos == None:
            self.pos = (0,0)
        self.color = color
        if self.color == None:
            self.color = (255,255,255)

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.pos, 20)


pg.font.init()
def get_font(size: int = 18, *args, **kwargs)->pg.font.Font:
    return pg.font.SysFont(kwargs.get("font"),size)

def create_ball(game: classBase.Base, kwargs: dict):
    game.objects.append(Ball(kwargs['pos'], kwargs['color']))

def controll_controll(game: classBase.Base,event: pg.event.Event):
    for ev in event:
        if ev.type == pg.MOUSEBUTTONUP:
            pos = (ev.pos[0]-5, ev.pos[1]-5)
            if ev.button == 3:   
                game.action['cascadepopup'] = {'pos': pos }
            if ev.button == 1:
                pass

        if ev.type == pg.MOUSEBUTTONDOWN:
            pos = (ev.pos[0]-5, ev.pos[1]-5)
            if ev.button == 1:
                game.cascade.on = False
                
                game.action['create_ball'] = {'pos': pos,
                                              'color':(255,0,0)}
        if ev.type == pg.QUIT:
            game.running = False

def cascadePopup(game: classBase.Base, kwargs: dict):
    #new_surf = game.cascade.draw_rect()
    new_surf = game.cascade.draw_surf()
    for a in game.cascade.cascade_options:
        new_surf.blit(a.surf, a.pos)

    game.cascade.pos = kwargs['pos']
    game.cascade.on = True
    game.cascade.surf = new_surf
    

class Cascade(classBase.CascadeBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.options = {'Create Ball': 0,
                        'Remove Ball': 1,
                        'Change color': 2,
                        'Exit': 4}
        self.font = get_font()
        self.font_color = (0,0,255)
        self.cascade_options = []
        if kwargs.get('font_color'):
            self.font_color = kwargs.get("font_color")

        self.font_offset = 1
        self.offset = 5
        self.draw_surf()


    def draw_surf(self):
        lenght = len(self.options.keys())
        grett = 0
        for a in self.options.keys():
            if len(a) >= grett:
                grett = len(a)
        height = (lenght*12) + self.offset
        width  = (grett * 8) + self.offset
        new_surf = Surface((width, height))
        new_surf.fill(self.color)
        self.create_options(new_surf)

        return new_surf
    

    def create_options(self, new_surf: Surface):
        pxY = 12
        cascade_count = 0
        actual_pxY = self.font_offset + (self.offset/2 )
        old_pxY = actual_pxY
        for a in self.options.keys():
            cascade_surf = pg.Surface((new_surf.size[0], pxY+(self.offset/2)), pg.SRCALPHA)
            cascade = CascadeOption(a, None, cascade_surf, (0,actual_pxY))
            cascade_surf.fill(cascade.color)
            txt_img = self.font.render( \
                        a, 
                        True,
                        self.font_color)
            cascade_surf.blit(txt_img, (self.offset,old_pxY))
            self.cascade_options.append(cascade)
            cascade_count += 1
            actual_pxY += pxY

class Main_Screen(classBase.Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pg.init()
        self.action_dict = {'cascadepopup': cascadePopup,
                            'create_ball': create_ball}
        self.size = (self.width, self.height)
        self.screen = pg.display.set_mode(self.size, pg.SRCALPHA)
        self.clock  = pg.time.Clock()
        self.action: dict[str, dict[str, tuple]] = {}
        self.running = True
        self.cascade = Cascade(color=(65,65,65), font_color=(255,255,255))
        self.objects = []

    def update(self):
        pg.display.flip()

    def exec_action(self):
        for action in self.action.keys():
            function = self.action_dict[action]
            function(self,self.action[action])
        self.action = {}

    def run(self):
        while self.running:
            controll_controll(self,pg.event.get())
            self.screen.fill(self.bg_color)
            
            if len(self.objects) > 0:
                new_surf = pg.Surface(self.size, pg.SRCALPHA)
                new_surf.fill((0,0,0,0))
                for _ in range(0, len(self.objects)):
                    self.objects[_].draw(new_surf)
                self.screen.blit(new_surf, (0,0))
            if len(self.action):
                self.exec_action()
            if self.cascade.on:
                if pg.mouse.get_pos()[0] > self.cascade.pos[0]:
                    for a in self.cascade.cascade_options:
                        if pg.mouse.get_pos()[1] < self.size[1] - a.pos[1]:
                            print("!")
                            a.old_color = a.color
                            a.color = a.hover_color 
                            break

                self.screen.blit(self.cascade.surf, self.cascade.pos)

            dt = self.clock.tick(60)
            pg.display.set_caption(str(dt))
            self.update()
            

if __name__ == "__main__":
    app = Main_Screen(bg_color=(200,200,0))
    try:
        app.run()
    except KeyboardInterrupt:
        pg.quit()
        print("Bye")

