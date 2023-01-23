from unittest import TestCase
from integrity import *


class IntegrityTest(TestCase):
    def test_mini_symmetry(self):
        # Note: none of these should be "offset", that will be tested later
        mini_grid = ['..XXX',
                     '.XXXX',
                     'XXXXX',
                     'XXXXX',
                     'XXXXX']
        self.assertEqual(None, check_rotational(mini_grid))
        self.assertEqual(None, check_reflection(mini_grid))
        self.assertEqual(mini_grid, check_diagonal(mini_grid))
        mini_grid = ['XXX..',  # checks other diagonal
                     'XXXX.',
                     'XXXXX',
                     'XXXXX',
                     '.XXXX']
        self.assertEqual(None, check_rotational(mini_grid))
        self.assertEqual(None, check_reflection(mini_grid))
        self.assertEqual(mini_grid, check_diagonal(mini_grid))
        mini_grid = ['..X..',
                     '.XXX.',
                     'XXXXX',
                     'XXXXX',
                     '.XXX.']
        self.assertEqual(None, check_rotational(mini_grid))
        self.assertEqual(mini_grid, check_reflection(mini_grid))
        self.assertEqual(None, check_diagonal(mini_grid))
        mini_grid = ['..XX.',
                     '.XXXX',
                     'XXXXX',
                     '.XXXX',
                     '..XX.']
        self.assertEqual(None, check_rotational(mini_grid))
        self.assertEqual(mini_grid, check_reflection(mini_grid))
        self.assertEqual(None, check_diagonal(mini_grid))
        mini_grid = ['..XX.',
                     '.XXXX',
                     'XXXXX',
                     'XXXX.',
                     '.XX..']
        self.assertEqual(mini_grid, check_rotational(mini_grid))
        self.assertEqual(None, check_reflection(mini_grid))
        self.assertEqual(mini_grid, check_diagonal(mini_grid))
        mini_grid = ['...XX',
                     '.XXXX',
                     'XXXXX',
                     'XXXX.',
                     'XX...']
        self.assertEqual(mini_grid, check_rotational(mini_grid))
        self.assertEqual(None, check_reflection(mini_grid))
        self.assertEqual(None, check_diagonal(mini_grid))
        mini_grid = ['...XX',
                     '.XXXX',
                     'XXXXX',
                     '.XXXX',
                     '...XX']
        self.assertEqual(None, check_rotational(mini_grid))
        self.assertEqual(mini_grid, check_reflection(mini_grid))
        self.assertEqual(None, check_diagonal(mini_grid))

    def test_offset(self):
        mini_grid = ['.....',
                     '...XX',
                     '.XXXX',
                     'XXXXX',
                     'XXXX.',
                     'XX...']
        self.assertEqual(mini_grid[1:], check_rotational(mini_grid))
        self.assertEqual(None, check_reflection(mini_grid))
        self.assertEqual(None, check_diagonal(mini_grid))
        mini_grid = ['..XXX',
                     '.XXXX',
                     'XXXXX',
                     'XXXX.',
                     'XXX..',
                     'XXXXX',
                     'XXXX.']
        self.assertEqual(mini_grid[:-2], check_rotational(mini_grid))
        self.assertEqual(None, check_reflection(mini_grid))
        self.assertEqual(mini_grid[:-2], check_diagonal(mini_grid))


    def test_supermega(self):
        # 2022 NYT Super Mega (with one error)
        expected = ['XXXXXXXXX.XXXXXXXXXXXXXX.XXXXXXXX.XXXXXX..XXXXX.XXXXXXXXX.XXXXXXXXX',
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
                    'XXXXXXXXX.XXXXXXXXX.XXXXX..XXXXXX.XXXXXXXX.XXXXXXXXXXXXXX.XXXXXXXXX']
        with open('supermegagrid.txt', 'r+') as f:
            grid = [line.strip('\n') for line in f.readlines()]
        self.assertEqual((expected, {'top':3, 'bottom':25, 'left':3, 'right': 3}), clean_edges(grid))
        self.assertEqual(expected, clean_edges(check_rotational(grid)))
        self.assertEqual(None, clean_edges(check_diagonal(grid)))
        self.assertEqual(None, clean_edges(check_reflection(grid)))

    def test_clean_edges_with_size(self):
        # NYT Mini 1/19/23
        mini_grid = ['..XXX',
                      '.XXXX',
                      'XXXXX',
                      'XXXXX',
                      'XXXXX']
        self.assertEqual(clean_edges(mini_grid, (5, 5)), expected)
        # I think symmetry should come before this step, so I need to do that before I go any further
