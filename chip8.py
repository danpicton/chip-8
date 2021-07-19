from time import sleep

import pygame, sys
from display import Display
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
PIXEL_SIZE = 12



class Chip8:

    def __init__(self, screen_res: tuple, pixel_size: int):
        self.memory = [None] * 4096 # 4k
        self.vregisters = [None] * 16 # 16
        self.pc = MEM_ADDRESS_START
        self.index = 0x00
        self.stack = [None] * 16 # 12 or 16
        self.sp = 0x00
        self.delay = 0xF
        self.bell = 0xF
        self.keypad = [None] * 16
        self.video = [[0]*screen_res[0] for _ in range(screen_res[1])]
        # self.video = [[0] * SCREEN_RES[0]] * SCREEN_RES[1]
        self.opcode = 0x00
        self.pixel_size = pixel_size
        self.screen_res = screen_res

        self.initialise()

    def __del__(self):
        pass

    def initialise(self):
        # load fonts
        self.pc = FONT_ADDRESS_START
        for b in FONTS:
            self.memory[self.pc] = b
            self.pc += 0x1
        self.pc = MEM_ADDRESS_START


    def load(self, rom_path):
        with open(rom_path, "rb") as f:

            while True:
                byte = f.read(1)
                if not byte: #eof
                    break
                self.memory[self.pc] = int.from_bytes(byte, byteorder='big')
                # print(byte)
                self.pc += 0x1

        f.close()
        self.pc = MEM_ADDRESS_START

    def fetch(self):
        # print(self.memory[self.pc])
        # print(self.memory[self.pc] << 8)
        # print(self.memory[self.pc+1])

        if self.memory[self.pc]:
            self.opcode = f"{self.memory[self.pc]:02x}" + f"{self.memory[self.pc + 1]:02x}" #TODO: load into memory as int
            self.pc+=2
        # read two bytes being pointed to by PC
        # increment PC by 2

    def decode(self):

        # print(f'{self.opcode} is a {type(self.opcode)}')
        instruction = self.opcode[0]
        X = int(self.opcode[1], 16)
        Y = int(self.opcode[2], 16)
        N = int(self.opcode[3], 16)
        NN = int(self.opcode[2:], 16)
        NNN = int(self.opcode[1:], 16)

        # big if/elseif statement with bit AND first char and rest
        # deconstruct bytes into nibbles [A, B, C, D] = 0XFF
        # execute instruction if no execute
        if self.opcode=='00e0':
            print("Clear screen")
            # print(f'x-1: {SCREEN_RES[0]}, y-1: {SCREEN_RES[1]}')
            for y in range(self.screen_res[1]):
                for x in range(self.screen_res[0]):
                    # print(f'Clearing: {x}, {y}')
                    # self.display.__draw_pixel(x, y, False)
                    self.video[y][x]=0

        elif instruction == '1':
            print(f'Jump to {NNN}')
            self.pc = NNN # come back to this
            pass
        elif instruction == '6':
            print(f'Set register {X} to {NN}')
            self.vregisters[X] = NN
        elif instruction == '7':
            print(f'Add {NN} to register {X}')
            self.vregisters[X] += NN
        elif instruction == 'a':
            print(f'Set index register, I, to {NNN}')
            self.index = NNN
        elif instruction == 'd':
            x=self.vregisters[X]
            y=self.vregisters[Y]
            print(f'Draw {N}-byte sprite from I at ({x}, {y})')

            for e, byte in enumerate(int(byte, 16) for byte in self.memory[self.index:self.index+N]):
                # print(f"byte {e}: {byte}")
                for e2, bit in enumerate(format(byte, "08b")):
                    # print(f"---> bit {e2}: {bit} - printing at {x+e2}, {y+e}")
                    self.video[y+e][x+e2] ^= int(bit)

        elif instruction != None:
            print(f'Different else - {self.opcode}')
        else:
            pass



def main(name):


    c = Chip8(SCREEN_RES, 8)
    display = Display(SCREEN_RES, PIXEL_SIZE)
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
    # c.video[10][10]=1
    # c.video[31][63]=1
    # c.video[20][29]=1
    # c.display.render_bitarray(c.video)
    # pygame.display.update()
    # sleep(0.5)

    # byte = 0xADCB
    #
    # n1,n2,n3,n4= byte & 0xF000, byte & 0x0F00, byte & 0x00F0, byte & 0x000F
    #
    # print(hex(n4))
    # print(hex(n3>>4))
    # print(hex(n2>>8))
    # print(hex(n1>>12))

    # c.load('test_opcode.ch8')
    c.load('ibm.ch8')

    pygame.init()
    pygame.display.set_caption("Chip8")

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        c.fetch()
        c.decode()
        sleep(0.1)
        display.render_bitarray(c.video)
        pygame.display.update()
    pass


# fetch
    # decode
    # execute (can be done in decode)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

