from pathlib import Path
from typing import List
from math import dist

class Polygon:
    def __init__(self):
        self.layer = None
        self.count = 0
        self.coord = []
        self.sides = []
    
    def set_layer(self, layer: int):
        self.layer = layer

    def add_coord(self, x: int, y: int):
        self.coord.append(tuple([x, y]))
    
    def find_sides(self):
        for i in range(1, self.count):
            self.sides.append(dist(self.coord[i-1], self.coord[i]))

class Source:
    def __init__(self, file_path: Path, output_path: Path) -> None:
        self.file_path = file_path / 'Source.txt' 
        self.output_path = output_path / 'output.txt'
        self.template_path = file_path / 'POI.txt'

        self.HEADER_SIZE = 8
        self.header = []
        self.body = []
        self.footer = []

        self.polygons: List[Polygon] = []
        self.template_polygons: List[Polygon] = []
        self.accepted_polygons = set()

    def read_source_file(self):
        with open(self.file_path, 'r') as reader:
            for i in range(self.HEADER_SIZE):
                self.header.append(reader.readline())

            while True:
                line = reader.readline()
                if line == "endstr\n":
                    self.footer.append(line)
                    break
                self.body.append(line)
            
            for line in reader.readlines():
                self.footer.append(line)
    
    def write_file(self) -> None:
        with open(self.output_path, 'w+') as writer:
            for line in self.header:
                writer.write(line)
            
            
            for curr_polygon in self.accepted_polygons:
                writer.write('boundary\n')
                writer.write(f'layer {curr_polygon.layer}\n')
                writer.write('datatype 0\n')
                writer.write(f'xy  {curr_polygon.count} ')

                for x, y in curr_polygon.coord:
                    writer.write(f' {x} {y} ')
                writer.write('\nendel\n')

            for line in self.footer:
                writer.write(line)
        print("Done", self.output_path.exists(), self.output_path)
    
    def load_template(self):
        body = []
        with open(self.template_path, 'r') as reader:
            for i in range(self.HEADER_SIZE):
                dump = reader.readline()

            while True:
                line = reader.readline()
                if line == "endstr\n":
                    break
                body.append(line)

        self.parse_template(body)

    def parse_template(self, body):
        curr_polygon = Polygon()
        for line in body:
            line: str = line.strip()
            if line == 'boundary':
                curr_polygon = Polygon()
            elif line == 'endel':
                curr_polygon.find_sides()
                self.template_polygons.append(curr_polygon)
            elif line.startswith('layer'):
                vals = line.split()
                curr_polygon.set_layer(int(vals[1]))
            elif line.startswith('datatype'):
                pass
            else:
                data = [i.strip() for i in line.split()]
                n = int(data[1])
                curr_polygon.count = n
                index = 2
                for i in range(n):
                    x, y = int(data[index]), int(data[index+1])
                    curr_polygon.add_coord(x, y)
                    index += 2

    def parse_body(self):
        curr_polygon = Polygon()
        for line in self.body:
            line: str = line.strip()
            if line == 'boundary':
                curr_polygon = Polygon()
            elif line == 'endel':
                curr_polygon.find_sides()
                self.polygons.append(curr_polygon)
            elif line.startswith('layer'):
                vals = line.split()
                curr_polygon.set_layer(int(vals[1]))
            elif line.startswith('datatype'):
                pass
            else:
                data = [i.strip() for i in line.split()]
                n = int(data[1])
                curr_polygon.count = n
                index = 2
                for i in range(n):
                    x, y = int(data[index]), int(data[index+1])
                    curr_polygon.add_coord(x, y)
                    index += 2
    
    def compare_polygons(self, template: Polygon, polygon: Polygon) -> bool:
        if template.layer != polygon.layer:
            return False

        if template.count != polygon.count:
            return False

        # Translate the points
        for ref in range(polygon.count):
            is_a_translated_template = True

            dx, dy = polygon.coord[ref][0] - template.coord[0][0], polygon.coord[ref][1] - template.coord[0][1]
            
            for index in range(template.count):
                tx, ty = template.coord[index]
                coord = polygon.coord[index]

                newx, newy = coord[0]-dx, coord[1]-dy
                
                if newx != tx or newy != ty:
                    is_a_translated_template = False
                    break

            if is_a_translated_template:
                return True

        # Compare the sides
        for shift in range(len(polygon.sides)):
            is_a_rotated_template = True
            shifted_sides = template.sides[shift:].copy()
            shifted_sides.extend(template.sides[: shift])
            
            for index in range(len(polygon.sides)):
                if polygon.sides[index] != shifted_sides[index]:
                    is_a_rotated_template = False
                    break
            
            if is_a_rotated_template:
                return True

        return False
    
    def identify_polygons(self):
        for polygon in self.polygons:
            for template in self.template_polygons:
                if self.compare_polygons(template, polygon):
                    self.accepted_polygons.add(polygon)

        print(len(self.accepted_polygons))
                