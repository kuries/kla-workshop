from pathlib import Path

INPUT_1 = "Milestone 1"
INPUT_2 = "Milestone 2"
INPUT_3 = "Milestone 3"
INPUT_4 = "Milestone 4"
INPUT_5 = "Milestone 5"
INPUT_6 = "Milestone 6"
INPUT_7 = "Milestone 7"

input_directory = Path('.\me\Milestone_Input\Milestone_Input')
output_directory = Path('.\me\Milestone_Output')

def get_directory_path(input=True, milestone_number=1):
    if input:
        directory = input_directory
    else:
        directory = output_directory

    if milestone_number == 1:
        new_path = (directory / INPUT_1)
    elif milestone_number == 2:
        new_path = (directory / INPUT_2)
    elif milestone_number == 3:
        new_path = (directory / INPUT_3)
    elif milestone_number == 4:
        new_path = (directory / INPUT_4)
    elif milestone_number == 5:
        new_path = (directory / INPUT_5)
    elif milestone_number == 6:
        new_path = (directory / INPUT_6)
    elif milestone_number == 7:
        new_path = (directory / INPUT_7)
    return new_path

def get_source(directory_path: Path):
    files = directory_path.glob('**/*')
    files = [x for x in files if x.is_file()]
    return files[0]