from enum import Enum
from typing import List, Optional
from malika_types import (
    Average,
    Categories,
    Columns,
    Participant,
)
from malika_utils import parse_file, make_column_names, make_participant_lines


if __name__ == "__main__":
    map_of_participants, map_of_averages = parse_file()

    new_file = open("a.out", "w")

    column_names = make_column_names(new_file)
    new_file.writelines(column_names)

    participant_values = make_participant_lines(map_of_participants, map_of_averages)
    new_file.writelines(participant_values)

    new_file.close()
