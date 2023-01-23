from pathlib import Path

from utils import get_directory_path, get_source
from source import Source

if __name__ == '__main__':
    input_path = get_directory_path(input=True, milestone_number=1)
    file_path = get_source(input_path)

    output_path = get_directory_path(input=False, milestone_number=1)

    s = Source(file_path, output_path)
    s.read_file()
    s.parse_body()
    s.write_file()
    pass