from unittest import TestCase
from read_text import read, extract_clues

class TextTest(TestCase):
    LAT_raw = "1/6/23, 5:40 AM L. A. Times, Tue, Jan 3, 2023 https://cdn4.amuselabs.com/lat/crossword-pdf 1/1L. A. Times, Tue, Jan 3, 2023 By Rebecca Goldstein / Ed. Patti Varol © 2023 Tribune Content Agency, LLC ACROSS 1Country music sound 6Coordinating pillowcase 10Roasting rod 14\"Yippee!\" 15Basketball commentator Rebecca 16Long-haired lap dog, familiarly 17Change with the times 18Major composition 19Working hard 20Smile broadly because of one's own achievement, say 23 Place for a scrub 24Devoutness 25 Grabbed a bite 28 Chicken __ king 30Red carpet walker 31Electric key 33New York City district that's home to the Fearless Girl statue 36Soup du __ 37Sign of spring 38Lead-in to Z or Alpha 39Koalas and emus, in Australia 40Novelist Atkinson 41Desirable feature of kids' clothing 43WSW oppositeDOWN44Prohibit 45Rowboat need 46Cap letters at Busch Stadium 47Get ready to drive? 49Mike and __: fruit- flavored candy 51Amino acid, vis-à-vis protein 56Aquarium growth 57Void's partner 58\"Ta-da!\" 61Thai currency 62Leave out 63\"Black-ish\" star Tracee __ Ross 64East, in Spanish 65Recedes 66Pomelo peels 1Pan Am rival 2Roll of dough 3Literary captain described as a \"grand, ungodly, god- like man\" 4Casual rejections 5Skated by, say 6React to a yellow light, say 7Indigenous language in Arizona 8Touch borders with 9Slam-dancer's place 10Emergency tire11Bite-sized treats whose name means \"small ovens\" in French 12\"Honest!\" 13Spot for un chapeau 21Home brewer's ingredient 22 Domino indent 25 Up and about 26 Some hairy pets 27Sweet Sixteen winners29 Alphabetically ﬁrst noble gas 30Mobile payment app 32Fighting chance? 34Director Spike 35Fair-hiring initials 36Spree 39Pay, reluctantly 41Soccer star and equal-pay advocate Megan42Donkey's need, in a party game 44Future flower 48Overjoy 50Common lab culture 51Paul Bunyan's blue ox 52Feeling nothing 53Smooth-talking 54Nonkosher sammies 55Potter's oven 59Jar topper 60Donkey1 2 3 4 5   6 7 8 9   10 11 12 13  14   15   16  17   18   19  20 21 22  23   24  25 26 27   28 29   30   31 32  33 34 35   36  37   38   39  40   41 42  43   44   45   46  47 48   49 50  51 52 53 54 55  56   57   58 59 60  61   62   63  64   65   66 "
    LAT_clues = {'across': [1, 6, 10, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 28, 30, 31, 33, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 47, 49, 51, 56, 57, 58, 61, 62, 63, 64, 65, 66],
                 'down': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 22, 25, 26, 27, 29, 30, 32, 34, 35, 36, 39, 41, 42, 44, 48, 50, 51, 52, 53, 54, 55, 59, 60]}

    def test_read(self):
        # this is fairly artificial so I'll keep it simple, but I'd want to know if it changed for some reason
        self.assertEqual(read('L. A. Times, Tue, Jan 3, 2023'), self.LAT_raw)

    def test_extract_clues(self):
        expected = 	{'across': ['Country music sound', 'Coordinating pillowcase', 'Roasting rod', '"Yippee!"', 'Basketball commentator Rebecca', 'Long-haired lap dog, familiarly', 'Change with the times', 'Major composition', 'Working hard', "Smile broadly because of one's own achievement, say", 'Place for a scrub', 'Devoutness', 'Grabbed a bite', 'Chicken __ king', 'Red carpet walker', 'Electric key', "New York City district that's home to the Fearless Girl statue", 'Soup du __', 'Sign of spring', 'Lead-in to Z or Alpha', 'Koalas and emus, in Australia', 'Novelist Atkinson', "Desirable feature of kids' clothing", 'WSW oppositeDOWN', 'Prohibit', 'Rowboat need', 'Cap letters at Busch Stadium', 'Get ready to drive?', 'Mike and __: fruit- flavored candy', 'Amino acid, vis-à-vis protein', 'Aquarium growth', "Void's partner", '"Ta-da!"', 'Thai currency', 'Leave out', '"Black-ish" star Tracee __ Ross', 'East, in Spanish', 'Recedes', 'Pomelo peels'],
                       'down': ['Pan Am rival', 'Roll of dough', 'Literary captain described as a "grand, ungodly, god- like man"', 'Casual rejections', 'Skated by, say', 'React to a yellow light, say', 'Indigenous language in Arizona', 'Touch borders with', "Slam-dancer's place", 'Emergency tire', 'Bite-sized treats whose name means "small ovens" in French', '"Honest!"', 'Spot for un chapeau', "Home brewer's ingredient", 'Domino indent', 'Up and about', 'Some hairy pets', 'Sweet Sixteen winners', 'Alphabetically ﬁrst noble gas', 'Mobile payment app', 'Fighting chance?', 'Director Spike', 'Fair-hiring initials', 'Spree', 'Pay, reluctantly', 'Soccer star and equal-pay advocate Megan', "Donkey's need, in a party game", 'Future flower', 'Overjoy', 'Common lab culture', "Paul Bunyan's blue ox", 'Feeling nothing', 'Smooth-talking', 'Nonkosher sammies', "Potter's oven", 'Jar topper', 'Donkey']}
        self.assertEqual(expected, extract_clues(self.LAT_raw, self.LAT_clues))

        modified_expected = 	{'across': ['Country music sound for R2-D2', 'Coordinating pillowcase', 'Roasting rod', '"Yippee!"', '1992 Basketball commentator Rebecca', 'Long-haired lap dog, familiarly', 'Change with the times', 'Major 1920 composition', 'Working hard', "Smile broadly because of one's own achievement, say", 'Place for a scrub', 'Devoutness', 'Grabbed a bite', 'Chicken __ king', 'Red carpet walker', 'Electric key', "New York City district that's home to the Fearless Girl statue", 'Soup du __', 'Sign of spring', 'Lead-in to Z or Alpha', 'Koalas and emus, in Australia', 'Novelist Atkinson', "Desirable feature of kids' clothing", 'WSW oppositeDOWN', 'Prohibit', 'Rowboat need', 'Cap letters at Busch Stadium', 'Get ready to drive?', 'Mike and __: fruit- flavored candy', 'Amino acid, vis-à-vis protein', 'Aquarium growth', "Void's partner", '"Ta-da!"', 'Thai currency', 'Leave out', '"Black-ish" star Tracee __ Ross', 'East, in Spanish', 'Recedes', 'Pomelo peels'],
                                'down': ['Pan Am (and C-3PO) rival', 'Roll of dough', 'Literary captain described as a "grand, ungodly, god- like man"', 'Casual rejections', 'Skated by, say', 'React to a yellow light, say', 'Indigenous language in Arizona', 'Touch borders with', "Slam-dancer's place", 'Emergency tire', 'Bite-sized treats whose name means "small ovens" in French', '"Honest!"', 'Spot for un 21st-century chapeau', "Home brewer's ingredient", 'Domino indent', 'Up and about', 'Some hairy pets', 'Sweet Sixteen winners', 'Alphabetically ﬁrst noble gas', 'Mobile payment app', 'Fighting chance?', 'Director Spike', 'Fair-hiring initials', 'Spree', 'Pay, reluctantly', 'Soccer star and equal-pay advocate Megan', "Donkey's need, in a party game", 'Future flower', 'Overjoy', 'Common lab culture', "Paul Bunyan's blue ox", 'Feeling nothing', 'Smooth-talking', 'Nonkosher sammies', "Potter's oven", 'Jar topper', 'Donkey']}
        modified_raw = "1/6/23, 5:40 AM L. A. Times, Tue, Jan 3, 2023 https://cdn4.amuselabs.com/lat/crossword-pdf 1/1L. A. Times, Tue, Jan 3, 2023 By Rebecca Goldstein / Ed. Patti Varol © 2023 Tribune Content Agency, LLC ACROSS 1Country music sound for R2-D2 6Coordinating pillowcase 10Roasting rod 14\"Yippee!\" 151992 Basketball commentator Rebecca 16Long-haired lap dog, familiarly 17Change with the times 18Major 1920 composition 19Working hard 20Smile broadly because of one's own achievement, say 23 Place for a scrub 24Devoutness 25 Grabbed a bite 28 Chicken __ king 30Red carpet walker 31Electric key 33New York City district that's home to the Fearless Girl statue 36Soup du __ 37Sign of spring 38Lead-in to Z or Alpha 39Koalas and emus, in Australia 40Novelist Atkinson 41Desirable feature of kids' clothing 43WSW oppositeDOWN44Prohibit 45Rowboat need 46Cap letters at Busch Stadium 47Get ready to drive? 49Mike and __: fruit- flavored candy 51Amino acid, vis-à-vis protein 56Aquarium growth 57Void's partner 58\"Ta-da!\" 61Thai currency 62Leave out 63\"Black-ish\" star Tracee __ Ross 64East, in Spanish 65Recedes 66Pomelo peels 1Pan Am (and C-3PO) rival 2Roll of dough 3Literary captain described as a \"grand, ungodly, god- like man\" 4Casual rejections 5Skated by, say 6React to a yellow light, say 7Indigenous language in Arizona 8Touch borders with 9Slam-dancer's place 10Emergency tire11Bite-sized treats whose name means \"small ovens\" in French 12\"Honest!\" 13Spot for un 21st-century chapeau 21Home brewer's ingredient 22 Domino indent 25 Up and about 26 Some hairy pets 27Sweet Sixteen winners29 Alphabetically ﬁrst noble gas 30Mobile payment app 32Fighting chance? 34Director Spike 35Fair-hiring initials 36Spree 39Pay, reluctantly 41Soccer star and equal-pay advocate Megan42Donkey's need, in a party game 44Future flower 48Overjoy 50Common lab culture 51Paul Bunyan's blue ox 52Feeling nothing 53Smooth-talking 54Nonkosher sammies 55Potter's oven 59Jar topper 60Donkey1 2 3 4 5   6 7 8 9   10 11 12 13  14   15   16  17   18   19  20 21 22  23   24  25 26 27   28 29   30   31 32  33 34 35   36  37   38   39  40   41 42  43   44   45   46  47 48   49 50  51 52 53 54 55  56   57   58 59 60  61   62   63  64   65   66 "
        self.assertEqual(modified_expected, extract_clues(modified_raw, self.LAT_clues))