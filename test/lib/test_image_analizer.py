import unittest
from app.lib.image_analizer import image_analizer


class TestImageAnalizer(unittest.TestCase):
    """
      test image_analizer.py 
      API request to AZURE VISION API
    """
    def test_image_analizer_class(self):
        """
          test image_analizer return list class
        """
        value=image_analizer('http://img.mcdonalds.co.jp/index/graphic/main_170920a.jpg')
        self.assertEqual(type(value), type([]))
        self.assertGreater(len(value), 0)
