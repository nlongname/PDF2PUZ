from unittest import TestCase
from grid import get_clue_numbers


class GridTest(TestCase):
    def test_clue_numbers(self):
        # L.A. Times, Tue, Jan 3, 2023
        test_grid = ['XXXXX.XXXX.XXXX',
                     'XXXXX.XXXX.XXXX',
                     'XXXXX.XXXX.XXXX',
                     '..XXXXXXXXXXXXX',
                     '...XXX...XXXXX.',
                     'XXX.XXX.XXX.XXX',
                     'XXXXXXXXXX.XXXX',
                     'XXXXX.XXX.XXXXX',
                     'XXXX.XXXXXXXXXX',
                     'XXX.XXX.XXX.XXX',
                     '.XXXXX...XXX...',
                     'XXXXXXXXXXXXX..',
                     'XXXX.XXXX.XXXXX',
                     'XXXX.XXXX.XXXXX',
                     'XXXX.XXXX.XXXXX']
        expected = {'across': [1, 6, 10, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 28, 30, 31, 33, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 47, 49, 51, 56, 57, 58, 61, 62, 63, 64, 65, 66],
                    'down': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 22, 25, 26, 27, 29, 30, 32, 34, 35, 36, 39, 41, 42, 44, 48, 50, 51, 52, 53, 54, 55, 59, 60]}
        self.assertEqual(expected, get_clue_numbers(test_grid))
        test_grid = ['XXXXX.XXXX.XXXX',
                     'XXXXX.XXXX.XXXX',
                     'XXXXX.XXXX.XXXX',
                     '..XXXXXXXXXXXXX',
                     '...XXX...XXXXX.',
                     'XXX.XXX.XXX.XXX',
                     'XXXXXXXXXX.XXXX',
                     'XXXXX.XXX.XXXXX',
                     'XXXX.XXXXXXXXXX',
                     'XXX.XXX.XXX.XXX',
                     '.XXXXX...XXX.X.',  # added a one-letter Across which shouldn't get clued or change Downs
                     'XXXXXXXXXXXXX..',  # ^this is a real mistake I've seen in the wild
                     'XXXX.XXXX.XXXXX',
                     'XXXX.XXXX.XXXXX',
                     'XXXX.XXXX.XXXXX']
        self.assertEqual(expected, get_clue_numbers(test_grid))
        donut_grid = ['12XXX3',
                      '4X...X',
                      '5X.6.X',
                      '7X.X.X',  # artificial version of a real (if rare) gimmick
                      'X....X',
                      '8XXXXX']
        expected = {'across': [1, 4, 5, 7, 8], 'down': [1, 2, 3, 6]}
        self.assertEqual(expected, get_clue_numbers(donut_grid))
