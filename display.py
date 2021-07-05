class Display():
    # PIXEL_SIZE = (8, 8)

    def __init__(self, chip8_resolution, pixel_size):
        self.width, self.height = (element * pixel_size for element in chip8_resolution)
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.pixel_size = pixel_size
        self.pixel_array = pygame.PixelArray(self.surface)

    def __draw_pixel(self, x, y, on=True):
        x*=self.pixel_size
        y*=self.pixel_size
        for py in range(self.pixel_size):
            for px in range(self.pixel_size):
                if on:
                    self.pixel_array[x+px, y+py] = 0xFFFFFF
                else:
                    self.pixel_array[x+px, y+py] = 0x000000

    def render_bitarray(self, bitarray):
        for iy, y in enumerate(bitarray):
            for ix, x in enumerate(bitarray[iy]):
                self.__draw_pixel(ix, iy, bool(x))