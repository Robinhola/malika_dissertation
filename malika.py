from enum import Enum
from typing import List
from dataclasses import dataclass

print("Hello")

class Columns(Enum):
    ParticipantID = 0
    ReactionTime = 1
    Correct = 2
    Congruency = 3
    Social_Non_Social = 4
    Block = 5
    Block_Number = 6

@dataclass
class Participant:
    id: str
    reaction_time: float
    congruency: bool
    sociality: bool
    block: str

    @classmethod
    def from_csv_line(cls, csv_line: str) -> "Participant":
        """Create participant from csv line"""
        line = csv_line.split(',')
        return Participant(
            id=line[Columns.ParticipantID.value],
            reaction_time=line[Columns.ReactionTime.value],
            congruency=line[Columns.Congruency.value] == "congruent",
            sociality=line[Columns.Social_Non_Social.value] == "Social",
            block=line[Columns.Block.value],
        )




def read_file() -> List[str]:
    """Read file for Malika"""
    file = open("Trial RT data_Socoff Simon Task.csv")
    lines: List[str] = file.readlines()
    file.close()
    return lines

def is_correct(csv_line: str):
    line: List[str] = csv_line.split(',')
    return line[Columns.Correct.value] == '1'

def remove_incorrect_answer(lines: List[str]) -> List[str]:
    """Remove lines that have incorrect answer (Column Correct == 0)"""
    csv_lines = lines[1:]
    return list(filter(is_correct, csv_lines))

lines = read_file()
correct_trials = remove_incorrect_answer(lines)
print(lines[110])
print(lines[109])
print(lines[108])
print("Correct")
print(correct_trials[110])
print(correct_trials[109])
print(correct_trials[108])
participants = [Participant.from_csv_line(csv_line) for csv_line in correct_trials]

from pprint import pprint
pprint(correct_trials[:2])
pprint(participants[:2])

# import pdb; pdb.set_trace()

