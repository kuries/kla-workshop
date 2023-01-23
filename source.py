from pathlib import Path

class Polygon:
    def __init__(self):
        self.layer = None
        self.coord = []
    
    def set_layer(self, layer: int):
        self.layer = layer

    def add_coord(self, x: int, y: int):
        self.coord.append(tuple([x, y]))

class Source:
    def __init__(self, file_path: Path, output_path: Path) -> None:
        self.file_path = file_path
        self.output_path = output_path / 'output.txt'
        self.HEADER_SIZE = 8
        self.header = []
        self.body = []
        self.footer = []

        self.polygons = []
        self.template_polygon = None

    def read_file(self):
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
            
            
            for curr_polygon in self.polygons[:2]:
                writer.write('boundary\n')
                writer.write(f'layer {curr_polygon.layer}\n')
                writer.write('datatype 0\n')
                writer.write(f'xy  {len(curr_polygon.coord)} ')

                for x, y in curr_polygon.coord:
                    writer.write(f' {x} {y} ')
                writer.write('\nendel\n')

            for line in self.footer:
                writer.write(line)
        print("Done", self.output_path.exists(), self.output_path)
    
    def parse_body(self):
        curr_polygon = Polygon()
        for line in self.body:
            line: str = line.strip()
            if line == 'boundary':
                curr_polygon = Polygon()
            elif line == 'endel':
                self.polygons.append(curr_polygon)
            elif line.startswith('layer'):
                vals = line.split()
                curr_polygon.set_layer(int(vals[1]))
            elif line.startswith('datatype'):
                pass
            else:
                data = [i.strip() for i in line.split()]
                n = int(data[1])
                index = 2
                for i in range(n):
                    x, y = int(data[index]), int(data[index+1])
                    curr_polygon.add_coord(x, y)
                    index += 2
