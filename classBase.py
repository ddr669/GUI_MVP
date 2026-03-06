class Base:
    width: int = 720
    height: int = 480
    bg_color: tuple = (0,0,0)
    running: bool = False
    action: dict = {}
    action_dict: dict = {}
    size: tuple = None
    clock = None
    objects = None
    def __init__(self, *args, **kwargs):
        self.width = self.width
        self.height = self.height
        self.bg_color = self.bg_color
        if 'width' in kwargs.keys():
            if isinstance(kwargs.get("width"), int):
                self.width = kwargs.get("width")
        if 'height' in kwargs.keys():
            if isinstance(kwargs.get("height"), int):
                self.height = kwargs.get("height")
        if 'size' in kwargs.keys():
            size = get_coord_from_kwargs(kwargs.get("size"))
            if size:
               self.width = size[0]
               self.height = size[1]
        if 'bg_color' in kwargs.keys():
            if isinstance(kwargs.get("bg_color"), tuple) or \
                    isinstance(kwargs.get("bg_color"), list):
                self.bg_color = kwargs.get("bg_color")

    def get_size(self)->tuple[int,int]:
        return (self.width, self.height)

class CascadeBase:
    def __init__(self, *args, **kwargs):
        self.on = False
        self.color = (0,255,0)
        if kwargs.get('color'):
            self.color = kwargs.get("color")
        self.surf = None
        self.pos = (0,0)


def get_coord_from_kwargs(size: tuple | list = None)->tuple[int,int]:
    if not size:
        return None
    if isinstance(size, tuple) or \
        isinstance(size, list):
        return size
    else:
        print(size)
        return None

if __name__ == "__main__":
    print("[!] This is a auxiliary script, try run the main script [!]")

