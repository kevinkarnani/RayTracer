from features.tuple import Color


class Canvas:
    def __init__(self, width, height, color=None):
        self.width = width
        self.height = height
        self.color = Color(0, 0, 0) if not color else color
        self.grid = [[self.color] * self.width for _ in range(self.height)]

    def write_pixel(self, x, y, color):
        self.grid[y][x] = color

    def pixel_at(self, x, y):
        return self.grid[y][x]

    def header(self):
        return f"P3\n{self.width} {self.height}\n255\n"

    def to_ppm(self):
        header = self.header()
        pixel_data = ""

        for row in self.grid:
            ppm_row = []
            for elem in row:
                (r, g, b) = elem.to_rgb()
                ppm_row.extend([r, g, b])
            # break into at most 17 elements per line to stay < 70 chars
            for line in [ppm_row[i: i + 17] for i in range(0, len(ppm_row), 17)]:
                pixel_data += " ".join(str(c) for c in line) + "\n"
        return header + pixel_data
