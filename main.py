from time import sleep

import pygame, sys
from pygame.locals import *
# memory 4k
# pc
# index register I (16)
# stack 12x 2 byte eg 0xFFFF
# delay timer
# sound timer
# 16 v registers (8)
FONT_ADDRESS_START = 0x050 # to 0x09F
MEM_ADDRESS_START = 0x200
FONTS = [
    0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
    0x20, 0x60, 0x20, 0x20, 0x70, # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
    0x90, 0x90, 0xF0, 0x10, 0x10, # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
    0xF0, 0x10, 0x20, 0x40, 0x40, # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90, # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
    0xF0, 0x80, 0x80, 0x80, 0xF0, # C
    0xE0, 0x90, 0x90, 0x90, 0xE0, # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
    0xF0, 0x80, 0xF0, 0x80, 0x80  # F
]
SCREEN_RES = (64, 32)



class Chip8:

    def __init__(self, display: pygame.display):
        self.memory = [None] * 4096 # 4k
        self.vregisters = [None] * 16 # 16
        self.pc = MEM_ADDRESS_START
        self.index = 0x00
        self.stack = [None] * 16 # 12 or 16
        self.sp = 0x00
        self.delay = 0xF
        self.bell = 0xF
        self.keypad = [None] * 16
        self.video = [None] * SCREEN_RES[0] * SCREEN_RES[1]
        self.opcode = 0x00
        self.display = display

        self.initialise()

    def initialise(self):
        # load fonts
        self.pc = FONT_ADDRESS_START
        for b in FONTS:
            self.memory[self.pc] = b
            self.pc += 0x1
        self.pc = MEM_ADDRESS_START


    def load(self, rom_path):
        with open(rom_path, "rb") as f:
            byte = f.read(1).hex()
            while byte != "":
                self.memory[self.pc] = byte
                # print(byte)
                self.pc += 0x1
                byte = f.read(1).hex()
        f.close()
        self.pc = MEM_ADDRESS_START

    def fetch(self):
        # print(self.memory[self.pc])
        # print(self.memory[self.pc] << 8)
        # print(self.memory[self.pc+1])

        if self.memory[self.pc]:
            self.opcode = self.memory[self.pc] + self.memory[self.pc + 1]
            self.pc+=2
        # read two bytes being pointed to by PC
        # increment PC by 2

    def decode(self):

        # print(f'{self.opcode} is a {type(self.opcode)}')
        instruction = self.opcode[0]
        X = self.opcode[1]
        Y = self.opcode[2]
        N = self.opcode[3]
        NN = self.opcode[2:]
        NNN = self.opcode[1:]

        # big if/elseif statement with bit AND first char and rest
        # deconstruct bytes into nibbles [A, B, C, D] = 0XFF
        # execute instruction if no execute
        if self.opcode=='00e0':
            print("Clear screen")
        elif instruction == '1':
            print(f'Jump to {NNN}')
        elif instruction == '6':
            print(f'Set register {X} to {NN}')
        elif instruction == '7':
            print(f'Add {NN} to register {X}')
        elif instruction == 'a':
            print(f'Set index register, I, to {NNN}')
        elif instruction == 'd':
            print(f'Draw {N} height sprite at ({X}, {Y})')
        elif instruction != None:
            print(f'Different else - {self.opcode}')
        else:
            pass

class Display:
    # PIXEL_SIZE = (8, 8)

    def __init__(self, chip8_resolution, pixel_size):
        pygame.init()
        self.width, self.height = (element * pixel_size for element in chip8_resolution)
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.pixel_size = pixel_size
        self.pixel_array = pygame.PixelArray(self.surface)
        pygame.display.set_caption("Chip8")

    def draw_pixel(self, x, y):
        x*=self.pixel_size
        y*=self.pixel_size
        for py in range(self.pixel_size - 1):
            for px in range(self.pixel_size - 1):
                self.pixel_array[x+px, y+py] = 0xFFFFFF

def main(name):

    d = Display(SCREEN_RES, 8)
    c = Chip8(d)
    # pygame.init()
    # DISPLAYSURF=pygame.display.set_mode((400,300))
    # # PIXELSIZE = [8,8]
    # target_xy={"x": 16, "y": 16}
    #
    # parr=pygame.PixelArray(DISPLAYSURF)
    # for cpy in range(PIXELSIZE[1]-1):
    #     for cpx in range(PIXELSIZE[0]-1):
    #
    #         parr[target_xy["x"]+cpx,target_xy["y"]+cpy]=0xFFFFFF
    d.draw_pixel(0,0)
    d.draw_pixel(1,1)
    d.draw_pixel(8,8)
    d.draw_pixel(63,31)
    pygame.display.update()
    sleep(2)

    # byte = 0xADCB
    #
    # n1,n2,n3,n4= byte & 0xF000, byte & 0x0F00, byte & 0x00F0, byte & 0x000F
    #
    # print(hex(n4))
    # print(hex(n3>>4))
    # print(hex(n2>>8))
    # print(hex(n1>>12))

    c.load('ibm.ch8')

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        c.fetch()
        c.decode()
        sleep(0.2)

        pygame.display.update()
    pass


# fetch
    # decode
    # execute (can be done in decode)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

