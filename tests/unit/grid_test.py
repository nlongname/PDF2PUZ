from unittest import TestCase
from grid import *
import os

class GridTest(TestCase):
    def test_grid_from_pic(self):
        file_list = os.listdir(os.getcwd())
        test_pdfs = ["Dictionary_2022-06-10", "NYT_1997-03-01", "Arkadium_2023-08-09", "L. A. Times, Tue, Jan 3, 2023",
                     "Puzzle WK4_2022-Ross"]  # , "NYT_SuperMegaCrossword_22"]
        dpis = [50, 100, 200]
        test_files = []
        for dpi in dpis:
            for filename in test_pdfs:
                if filename + f"_{dpi}.png" not in file_list:
                    pic = convert_from_path(f"{filename}.pdf", dpi=dpi, fmt="png")[0]
                    print(dpi, filename)
                    pic.save(f"{filename}_{dpi}.png", 'PNG')
                test_files.append((dpi, filename))
        expected = {"L. A. Times, Tue, Jan 3, 2023": ['XXXXX.XXXX.XXXX',
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
                                                      'XXXX.XXXX.XXXXX'],
                    "NYT_SuperMegaCrossword_22": ['XXXXXXXXX.XXXXXXXXXXXXXX.XXXXXXXX.XXXXXX..XXXXX.XXXXXXXXX.XXXXXXXXX',
                                                  'XXXXXXXXX.XXXXXXXXXXXXXX.XXXXXXXX.XXXXXX.XXXXXX.XXXXXXXXX.XXXXXXXXX',
                                                  'XXXXXXXXX.XXXXXXXXXXXXXX.XXXXXXXX.XXXXXX.XXXXXX.XXXXXXXXX.XXXXXXXXX',
                                                  'XXXXX.XXXX.XXXXX.XXX.XXXXXXX.XXXXXXXXXXXXXXXXXX.XXXXXXXXXXX.XXXXXXX',
                                                  '.XXX....XXXX..XXXXXXX.XXXXXXX....XXXXX..XXXX..XXXXXX..XXXXX...XXX..',
                                                  '..XXX.XXXXXXXXXXX.XXXX.XXXX.XXXXXXXXX.XXXXX.XXXXX.XXXX.XXXXXXXXXXXX',
                                                  'XXX.XXXX.XXXXX.XXXXXXXXXX..XXXXXXXX..XXXX.XXXXXX.XXXXXX.XXXXXX..XXX',
                                                  'XXX.XXXXX..XXXX.XXXXXXX.XXXXXXXXXX.XXXXXXX.XXXXXXX.XXXXXXXXXXXX.XXX',
                                                  'XXXXXXXXXXX.XXXX.XXX.XXX.XXX.XXXX.XXXXXX.XXXXX.XXXX..XXXXXXXX.XXXXX',
                                                  'XXXXX.XXXXX...XXXXX.XXXXXXXXX.....XXXX.XXXXXXX.XXXXXXXXX.XXX.XXXXXX',
                                                  'XXXXXX.XXXX.XXXXX..XXXXXXXX.XXXXXXX.XXXXX.XXXXX.XXXXXXX...XXXXXXXXX',
                                                  'XXXXXXX.XXXXXXXXXXXXXX.XXXX.XXXXXXX.XXXXXX.XXXXX.XXXX.XXXX.XXXXX...',
                                                  '...XXXXX.XXXXXX.XXXXX.XXXXX.XXXXXXXXXXX.XXXXXXXXX.XXXX.XXXXXX.XXXXX',
                                                  'XXX.XXXXX.XXX.XXXXXX.XXXXXXX.XXXXX.XXXXX.XXXXX.XXX.XXX.XXXXXXX.XXXX',
                                                  'XXXXXXXXXXXX.XXXXXX.XXXXX.XXXXXXXXXXX.XXXXXX..XXXX.XXXX.XXXXXXX.XXX',
                                                  'XXXXX.XXXXX.XXXXX.XXXXXX.XXXXXXX.XXX.XXXXXX.XXXXXXXXXXXX.XXX.XXXXXX',
                                                  'XXXX.XXXXX.XXXXXX..XXXX.XXXXXXXX..XXXXXXXX.XXXX..XXXX.XXXX.XXXXXXXX',
                                                  'XXXXXXXX.XXXXXX.XXXXXX.XXXXXXXX.XXXXXXXXX.XXXXXXXXX.XXXXX.XXXXXXXX.',
                                                  '...XXX.XXXXXXXX.XXXXX.XXXXXXXX.XXXXXXXXX.XXXXXXXXX.XXXXXX.XXXX..XXX',
                                                  'XXXXX.XXXXXXX.XXXXXX.XXXXXXXX.XXXX.XXXX.XXXXXXXXX.XXXXX.XXXXX.XXXXX',
                                                  'XXXXX.XXXXXX.XXXXXX.XXX.XXXX.XXXXXXXXX.XXXX.XXX.XXXXXX.XXXXXX.XXXXX',
                                                  'XXXXX.XXXXX.XXXXX.XXXXXXXXX.XXXX.XXXX.XXXXXXXX.XXXXXX.XXXXXXX.XXXXX',
                                                  'XXX..XXXX.XXXXXX.XXXXXXXXX.XXXXXXXXX.XXXXXXXX.XXXXX.XXXXXXXX.XXX...',
                                                  '.XXXXXXXX.XXXXX.XXXXXXXXX.XXXXXXXXX.XXXXXXXX.XXXXXX.XXXXXX.XXXXXXXX',
                                                  'XXXXXXXX.XXXX.XXXX..XXXX.XXXXXXXX..XXXXXXXX.XXXX..XXXXXX.XXXXX.XXXX',
                                                  'XXXXXX.XXX.XXXXXXXXXXXX.XXXXXX.XXX.XXXXXXX.XXXXXX.XXXXX.XXXXX.XXXXX',
                                                  'XXX.XXXXXXX.XXXX.XXXX..XXXXXX.XXXXXXXXXXX.XXXXX.XXXXXX.XXXXXXXXXXXX',
                                                  'XXXX.XXXXXXX.XXX.XXX.XXXXX.XXXXX.XXXXX.XXXXXXX.XXXXXX.XXX.XXXXX.XXX',
                                                  'XXXXX.XXXXXX.XXXX.XXXXXXXXX.XXXXXXXXXXX.XXXXX.XXXXX.XXXXXX.XXXXX...',
                                                  '...XXXXX.XXXX.XXXX.XXXXX.XXXXXX.XXXXXXX.XXXX.XXXXXXXXXXXXXX.XXXXXXX',
                                                  'XXXXXXXXX...XXXXXXX.XXXXX.XXXXX.XXXXXXX.XXXXXXXX..XXXXX.XXXX.XXXXXX',
                                                  'XXXXXX.XXX.XXXXXXXXX.XXXXXXX.XXXX.....XXXXXXXXX.XXXXX...XXXXX.XXXXX',
                                                  'XXXXX.XXXXXXXX..XXXX.XXXXX.XXXXXX.XXXX.XXX.XXX.XXX.XXXX.XXXXXXXXXXX',
                                                  'XXX.XXXXXXXXXXXX.XXXXXXX.XXXXXXX.XXXXXXXXXX.XXXXXXX.XXXX..XXXXX.XXX',
                                                  'XXX..XXXXXX.XXXXXX.XXXXXX.XXXX..XXXXXXXX..XXXXXXXXXX.XXXXX.XXXX.XXX',
                                                  'X.XXXXXXXXXX.XXXX.XXXXX.XXXXX.XXXXXXXXX.XXXX.XXXX.XXXXXXXXXXX.XXX..',
                                                  '..XXX...XXXXX..XXXXXX..XXXX..XXXXX....XXXXXXX.XXXXXXX..XXXX....XXX.',
                                                  'XXXXXXX.XXXXXXXXXXX.XXXXXXXXXXXXXXXXXX.XXXXXXX.XXX.XXXXX.XXXX.XXXXX',
                                                  'XXXXXXXXX.XXXXXXXXX.XXXXXX.XXXXXX.XXXXXXXX.XXXXXXXXXXXXXX.XXXXXXXXX',
                                                  'XXXXXXXXX.XXXXXXXXX.XXXXXX.XXXXXX.XXXXXXXX.XXXXXXXXXXXXXX.XXXXXXXXX',
                                                  'XXXXXXXXX.XXXXXXXXX.XXXXX..XXXXXX.XXXXXXXX.XXXXXXXXXXXXXX.XXXXXXXXX'],
                    'Dictionary_2022-06-10': ['XXXX.XXXXX.XXX.',
                                              'XXXX.XXXXX.XXXX',
                                              'XXXX.XXXXXXXXXX',
                                              'XXXXXX.XXXX.XXX',
                                              '..XXX.XXXXXXXXX',
                                              'XXXXXXX.XXXX...',
                                              'XXXXXXXX..XXXXX',
                                              'XXX..XXXXX..XXX',
                                              'XXXXX..XXXXXXXX',
                                              '...XXXX.XXXXXXX',
                                              'XXXXXXXXX.XXX..',
                                              'XXX.XXXX.XXXXXX',
                                              'XXXXXXXXXX.XXXX',
                                              'XXXX.XXXXX.XXXX',
                                              '.XXX.XXXXX.XXXX'],
                    'Puzzle WK4_2022-Ross': ['XXXX.XXXXX.XXXX',
                                             'XXXX.XXXXX.XXXX',
                                             'XXXX.XXXXX.XXXX',
                                             'XXX.XXXXXXX.XXX',
                                             'XXXXX.XXX.XXXXX',
                                             '.XXXX.XXX.XXXX.',
                                             'XXXX.XXXXX.XXXX',
                                             'XXXX.XXXXX.XXXX',
                                             'XXXXXX...XXXXXX',
                                             'XXXXX.XXX.XXXXX',
                                             'XXX.XXXXXXX.XXX',
                                             '...XXXXXXXXX...',
                                             'XXXXXXXXXXXXXXX',
                                             'XXXX.XXXXX.XXXX',
                                             'XXXX.XXXXX.XXXX'],
                    'Arkadium_2023-08-09': ['XXXX.XXXX.XXXXX',
                                            'XXXX.XXXX.XXXXX',
                                            'XXXX.XXXX.XXXXX',
                                            'XXXXXXXXXXXXX..',
                                            'XXXXX..XXX..XXX',
                                            'XXXXXXX..XXXXXX',
                                            '.....XXXX.XXXXX',
                                            'XXXXXXXXXXXXXXX',
                                            'XXXXX.XXXX.....',
                                            'XXXXXX..XXXXXXX',
                                            'XXX..XXX..XXXXX',
                                            '..XXXXXXXXXXXXX',
                                            'XXXXX.XXXX.XXXX',
                                            'XXXXX.XXXX.XXXX',
                                            'XXXXX.XXXX.XXXX'],
                    'NYT_1997-03-01': ['XXXXX.XXXX..XXX',
                                       'XXXXX.XXXX.XXXX',
                                       'XXXXX.XXXX.XXXX',
                                       'XXX.XXXX..XXXXX',
                                       '...XXX.XXXXXXX.',
                                       'XXXXXXX.XXXX...',
                                       'XXXXX.XXXX.XXXX',
                                       'XXX..XXXXX..XXX',
                                       'XXXX.XXXX.XXXXX',
                                       '...XXXX.XXXXXXX',
                                       '.XXXXXXX.XXX...',
                                       'XXXXX..XXXX.XXX',
                                       'XXXX.XXXX.XXXXX',
                                       'XXXX.XXXX.XXXXX',
                                       'XXX..XXXX.XXXXX']
                    }
        for file in test_files:
            dpi, filename = file
            print(dpi, filename)
            test_grid = grid_from_pic(f"{filename}_{dpi}.png", dpi=dpi)
            self.assertEqual(expected[filename], test_grid)


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
