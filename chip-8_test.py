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



    # @video_test(screen_res=(10, 12), pixel_size=8)
    def test_video_array_y(self):
        c = Chip8((10, 12), 8)

        self.assertEqual(len(c.video), 12)

        del c

    def test_video_array_x(self):
        c = Chip8((36, 8), 8)

        self.assertEqual(len(c.video[0]), 36)

    @non_video_test
    def test_fetch(self, c):

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
        c = Chip8((20, 20), 8)

        for i in range(10):
            c.video[randint(0,18)+1][randint(0,18)+1] = 1

        c.opcode='00e0'
        c.decode()

        self.assertEqual(sum(list(map(sum, c.video))), 0)

        del c

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
