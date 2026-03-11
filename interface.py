import pygame as pg
#from pygame import font as FONT
import classBase

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
    lenght = len(game.cascade.options.keys())
    grett = 0
    for a in game.cascade.options.keys():
        if len(a) >= grett:
            grett = len(a)
    height = (lenght*12) + game.cascade.offset
    width  = (grett * 8) + game.cascade.offset

    new_surf = pg.Surface((width, height))
    new_surf.fill(game.cascade.color)
    pxY = 12
    actual_pxY = game.cascade.font_offset + (game.cascade.offset/2 )
    for a in game.cascade.options.keys():
        txt_img = game.cascade.font.render( \
                    a, 
                    True,
                    game.cascade.font_color)
        new_surf.blit(txt_img, (game.cascade.offset,actual_pxY))
        actual_pxY += pxY
    
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
        if kwargs.get('font_color'):
            self.font_color = kwargs.get("font_color")

        self.font_offset = 1
        self.offset = 5

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

