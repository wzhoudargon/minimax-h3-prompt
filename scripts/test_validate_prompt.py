"""Regression checks for mode routing; no provider calls or media generation."""
import unittest
from validate_prompt import validate

BODY = ('integrated_multimodal_description: [Shot 1] A cup stands on a table.\n\n'
        'overall_soundscape: Quiet room.\n\nnon_diegetic_music: N/A')
FIRST = ('For the target video, at 0.00 seconds into the target video, '
         '<Picture 1> (from [Shot 1]) is fully referenced.\n\n')
PAIR = ('How the reference pictures align with the target video — Picture 1 '
        '(from Shot 1) aligns with the 0.00-second mark of the target video; '
        'Picture 2 (from Shot 2) aligns with the 8.00-second mark of the target video.\n\n')
LAST = ('How the reference pictures align with the target video — <Picture 1> '
        '(from [Shot 2]) aligns with the 8.00-second mark of the target video.\n\n')
TWO = BODY.replace('A cup stands on a table.', 'A cup is lifted. [Shot 2] The cup returns to the table.')


class RoutingTests(unittest.TestCase):
    def test_supported_modes(self):
        for text, mode, count in [(BODY, 'T2VA', 0), (FIRST+BODY, 'I2VA', 1),
                                  (PAIR+TWO, 'FL2VA', 2), (LAST+TWO, 'L2VA', 1)]:
            with self.subTest(mode=mode):
                self.assertEqual(validate(text, mode, 8, count), [])

    def test_wrong_mode_or_asset_count(self):
        self.assertTrue(validate(FIRST+BODY, 'T2VA', 8, 0))
        self.assertTrue(validate(FIRST+BODY, 'I2VA', 8, 2))
        self.assertTrue(validate(BODY, 'I2VA', 8, 1))

    def test_last_shot_and_end_time(self):
        self.assertTrue(validate(PAIR+BODY, 'FL2VA', 8, 2))
        self.assertTrue(validate(LAST+TWO, 'L2VA', 9, 1))
        self.assertTrue(validate(PAIR+TWO.replace('[Shot 2]', '[Shot 3]'), 'FL2VA', 8, 2))

    def test_fields_and_header_position(self):
        self.assertTrue(validate('Title\n'+FIRST+BODY, 'I2VA', 8, 1))
        self.assertTrue(validate(FIRST+BODY+'\noverall_soundscape: wind', 'I2VA', 8, 1))
        self.assertTrue(validate(FIRST+BODY.replace('Quiet room.', ''), 'I2VA', 8, 1))

    def test_missing_assets_and_limits(self):
        self.assertTrue(validate(FIRST+BODY.replace('A cup', 'Picture 2: a cup'), 'I2VA', 8, 1))
        self.assertTrue(validate(BODY, 'T2VA', float('nan'), 0))
        self.assertTrue(validate(BODY, 'T2VA', 8, 0, 5))

    def test_no_poetry_or_english_only_rule(self):
        text = FIRST+BODY.replace('A cup stands on a table.', '两位角色对话，人物A说：“你好。”人物B回答：“你好。”')
        self.assertEqual(validate(text, 'I2VA', 8, 1), [])


if __name__ == '__main__':
    unittest.main()
