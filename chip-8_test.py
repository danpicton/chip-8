import unittest
from random import randint
from chip8 import Chip8

# Factory for decorators
def video_test(screen_res, pixel_size):
    def do_test_wrapped(func):
        def do_test(self):
            test_chip8 = Chip8(screen_res, pixel_size)

            func(self, test_chip8)

            del test_chip8

        return do_test

    return do_test_wrapped

def non_video_test(func):
    def do_test(self):
        test_chip8 = Chip8((1, 1), 1)

        func(self, test_chip8)

        del test_chip8

    return do_test


class TestChip8(unittest.TestCase):

    @video_test((10, 12), 8)
    def test_video_array_y(self, c):

        self.assertEqual(len(c.video), 12)

    @video_test((36, 8), 8)
    def test_video_array_x(self, c):

        self.assertEqual(len(c.video[0]), 36)

    @non_video_test
    def test_fetch(self, c):

        c.pc = 0
        c.memory = [255, 76, 126, 237, 1]
        c.fetch()

        self.assertEqual(c.opcode, 331)

    @video_test((20, 20), 8)
    def test_decode_00e0(self, c):

        for i in range(10):
            c.video[randint(0,18)+1][randint(0,18)+1] = 1

        c.opcode='00e0'
        c.decode()

        self.assertEqual(sum(list(map(sum, c.video))), 0)


    @non_video_test
    def test_decode_1NNN(self, c):
        c.opcode = '12ef'
        c.decode()

        self.assertEqual(c.pc, int('2ef', 16))

    @non_video_test
    def test_decode_7XNN(self, c):
        c.vregisters[3] = 0x3f

        c.opcode = '730a'
        c.decode()

        self.assertEqual(c.vregisters[3], 0x3f + 0x0a)

    @non_video_test
    def test_decode_aNNN(self, c):
        c.opcode = 'a1ef'
        c.decode()

        self.assertEqual(c.index, 0x1ef)

    @video_test((10, 10), 8)
    def test_decode_dXYN(self, c):
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

if __name__ == '__main__':
    unittest.main()
