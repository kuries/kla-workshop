from pathlib import Path

from utils import get_directory_path, get_source
from source import Source

if __name__ == '__main__':
    input_path = get_directory_path(input=True, milestone_number=3)

    output_path = get_directory_path(input=False, milestone_number=3)

    s = Source(input_path, output_path)
    s.read_source_file()
    s.parse_body()
    s.load_template()
    s.identify_polygons()
    s.write_file()
    pass