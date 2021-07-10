import unittest
from random import randint

import chip8
from chip8 import Chip8, Display

class TestChip8(unittest.TestCase):



    def test_video_array_y(self):
        c = Chip8((10, 12), 8)

        self.assertEqual(len(c.video), 12)

        del c

    def test_video_array_x(self):
        c = Chip8((36, 8), 8)

        self.assertEqual(len(c.video[0]), 36)

    def test_fetch(self):
        c = Chip8((1, 1), 8)
        c.pc = 0
        c.memory = [255, 76, 126, 237, 1]
        c.fetch()

        self.assertEqual(c.opcode, 331)

        del c

    # def test_decode(self):
    #     c = Chip8((1, 1))
    #     c.pc = 0
    #     c.memory = [255, 76, 126, 237, 1]
    #     c.fetch()
    #     c.decode()
    #
    #     self.assertEqual()

    def test_decode_00e0(self):
        c = Chip8((20, 20), 8)

        for i in range(10):
            c.video[randint(0,18)+1][randint(0,18)+1] = 1

        c.opcode='00e0'
        c.decode()

        self.assertEqual(sum(list(map(sum, c.video))), 0)

        del c

    def test_decode_1NNN(self):
        c = Chip8((1, 1), 8)

        c.opcode = '12ef'
        c.decode()

        self.assertEqual(c.pc, int('2ef', 16))

        del c

    def test_decode_7XNN(self):
        c = Chip8((1, 1), 1)

        c.vregisters[3] = 0x3f

        c.opcode = '730a'
        c.decode()

        self.assertEqual(c.vregisters[3], 0x3f + 0x0a)

        del c

    def test_decode_aNNN(self):
        c = Chip8((1, 1), 1)

        c.opcode = 'a1ef'
        c.decode()

        self.assertEqual(c.index, 0x1ef)

        del c

    def test_decode_dXYN(self):
        c = Chip8((10, 10), 8)
        c.memory = list(hex(hexbyte) for hexbyte in [0, 0, 0, 1, 2, 4, 8, 16, 32, 64, 128, 7, 3])
        c.vregisters[3] = 0x0
        c.vregisters[5] = 0x0
        c.index = 3
        c.opcode='d358'
        c.decode()

        expected = [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.assertEqual(c.video, expected)

        del c

if __name__ == '__main__':
    unittest.main()
