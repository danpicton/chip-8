import unittest
from random import randint

import chip8
from chip8 import Chip8, Display

class TestChip8(unittest.TestCase):



    def test_video_array_y(self):
        c = Chip8((64, 32))

        self.assertEqual(len(c.video), 32)

    def test_video_array_x(self):
        c = Chip8((64, 32))

        self.assertEqual(len(c.video[0]), 64)

    def test_fetch(self):
        c = Chip8((1, 1))
        c.pc = 0
        c.memory = [255, 76, 126, 237, 1]
        c.fetch()

        self.assertEqual(c.opcode, 331)

    # def test_decode(self):
    #     c = Chip8((1, 1))
    #     c.pc = 0
    #     c.memory = [255, 76, 126, 237, 1]
    #     c.fetch()
    #     c.decode()
    #
    #     self.assertEqual()

    def test_decode_00e0(self):
        c = Chip8((20, 20))
        for i in range(10):
            c.video[randint(0,18)+1][randint(0,18)+1] = 1

        c.opcode='00e0'
        c.decode()

        self.assertEqual(sum(list(map(sum, c.video))), 0)

    def test_decode_1NNN(self):
        pass

    def test_decode_7XNN(self):
        pass

    def test_decode_aNNN(self):
        pass

    def test_decode_dXYN(self):
        pass

if __name__ == '__main__':
    unittest.main()
