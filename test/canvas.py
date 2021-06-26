import unittest

from features.canvas import Canvas
from features.tuple import *


class TestCanvas(unittest.TestCase):
    def test_canvas(self):
        c = Canvas(10, 20)
        self.assertEqual(c.width, 10)
        self.assertEqual(c.height, 20)
        for row in c.grid:
            self.assertEqual(row, [Color(0, 0, 0)] * c.width)

    def test_write(self):
        c = Canvas(10, 20)
        c.write_pixel(2, 3, Color(1, 0, 0))
        self.assertEqual(c.pixel_at(2, 3), Color(1, 0, 0))

    def test_ppm_headers(self):
        canvas = Canvas(5, 3)
        ppm = canvas.to_ppm().splitlines()
        header = [s.strip() for s in ppm][0:3]
        expected_header = ["P3", "5 3", "255"]
        self.assertEqual(header, expected_header)

    def test_pixel_data(self):
        canvas = Canvas(5, 3)
        canvas.write_pixel(0, 0, Color(1.5, 0, 0))
        canvas.write_pixel(2, 1, Color(0, 0.5, 0))
        canvas.write_pixel(4, 2, Color(-0.5, 0, 1))
        ppm = canvas.to_ppm().splitlines()
        pixel_data = [s.strip() for s in ppm][3:6]
        expected_data = [
            "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 0 0 0 0 0 0 128 0 0 0 0 0 0 0",
            "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255",
        ]
        self.assertEqual(pixel_data, expected_data)

    def test_line_length(self):
        canvas = Canvas(10, 2, Color(1, 0.8, 0.6))
        ppm = canvas.to_ppm().splitlines()
        pixel_data = [s.strip() for s in ppm][3:7]
        expected_data = [
            "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204",
            "153 255 204 153 255 204 153 255 204 153 255 204 153",
            "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204",
            "153 255 204 153 255 204 153 255 204 153 255 204 153",
        ]
        self.assertEqual(pixel_data, expected_data)

    def test_EOF(self):
        canvas = Canvas(5, 3)
        ppm = canvas.to_ppm()
        self.assertTrue(ppm.endswith("\n"))





