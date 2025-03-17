#region ============================ Imports =============================

import unittest
import sys
import os

# Add the project root to PYTHONPATH for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from System.Rendering.FragmentCanvas import FragmentCanvas


#endregion



class TestFragmentCanvas(unittest.TestCase):
    def setUp(self):
        """ Initialize test data """
        self.test_scene_str_A = """
        AAAAAAA
        BBBBBBB
        CCCCCCC
        DDDDDDD
        EEEEEEE
        FFFFFFF
        GGGGGGG""".strip().replace(' ', '')         # strip() to remove leading newline

        self.test_scene_str_B = """
        aaaa
        bbbb
        cccc
        dddd
        eeee""".strip().replace(' ', '')


    def test_draw(self):
        """Test the in-place draw method"""

        # Test 1: normal filling from (0, 0)

        draw_coords_1 = (0, 0)
        draw_result_str_1 = """
        aaaaAAA
        bbbbBBB
        ccccCCC
        ddddDDD
        eeeeEEE
        FFFFFFF
        GGGGGGG""".strip().replace(' ', '')

        fragment = FragmentCanvas.from_string(self.test_scene_str_A)
        fragment.draw(draw_coords_1, self.test_scene_str_B)
        self.assertEqual(fragment.to_string(), draw_result_str_1)

        # Test 2: enclosed filling

        draw_coords_2 = (1, 1)
        draw_result_str_2 = """
        AAAAAAA
        BaaaaBB
        CbbbbCC
        DccccDD
        EddddEE
        FeeeeFF
        GGGGGGG""".strip().replace(' ', '')

        fragment = FragmentCanvas.from_string(self.test_scene_str_A)
        fragment.draw(draw_coords_2, self.test_scene_str_B)
        self.assertEqual(fragment.to_string(), draw_result_str_2)

        # Test 3: out-of-bounds filling (lower-right corner)

        draw_coords_3 = (-1, 4)
        draw_result_str_3 = """
        AAAAAAA
        BBBBBBB
        CCCCCCC
        DDDDDDD
        aaaEEEE
        bbbFFFF
        cccGGGG""".strip().replace(' ', '')

        fragment = FragmentCanvas.from_string(self.test_scene_str_A)
        fragment.draw(draw_coords_3, self.test_scene_str_B)
        self.assertEqual(fragment.to_string(), draw_result_str_3)

        # Test 4: out-of-bounds filling (top-right corner)

        draw_coords_4 = (5, -1)
        draw_result_str_4 = """
        AAAAAbb
        BBBBBcc
        CCCCCdd
        DDDDDee
        EEEEEEE
        FFFFFFF
        GGGGGGG""".strip().replace(' ', '')

        fragment = FragmentCanvas.from_string(self.test_scene_str_A)
        fragment.draw(draw_coords_4, self.test_scene_str_B)
        self.assertEqual(fragment.to_string(), draw_result_str_4)

if __name__ == '__main__':
    unittest.main(verbosity=2)
