from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class Columns(Enum):
    ParticipantID = 0
    ReactionTime = 1
    Correct = 2
    Congruency = 3
    Social_Non_Social = 4
    Block = 5
    Block_Number = 6


class Categories(Enum):
    SocialCongruentFirstblock = 111
    SocialCongruentSecondblock = 112
    SocialIncongruentFirstblock = 121
    SocialIncongruentSecondblock = 122
    NonSocialCongruentFirstblock = 211
    NonSocialCongruentSecondblock = 212
    NonSocialIncongruentFirstblock = 221
    NonSocialIncongruentSecondblock = 222


def find_category(line: List[str]) -> Categories:
    if (
        line[Columns.Social_Non_Social.value] == "Social"
        and line[Columns.Congruency.value] == "congruent"
        and line[Columns.Block.value] == "First"
    ):
        return Categories.SocialCongruentFirstblock

    if (
        line[Columns.Social_Non_Social.value] == "Social"
        and line[Columns.Congruency.value] == "congruent"
        and line[Columns.Block.value] == "Second"
    ):
        return Categories.SocialCongruentSecondblock

    if (
        line[Columns.Social_Non_Social.value] == "Social"
        and line[Columns.Congruency.value] == "incongruent"
        and line[Columns.Block.value] == "First"
    ):
        return Categories.SocialIncongruentFirstblock

    if (
        line[Columns.Social_Non_Social.value] == "Social"
        and line[Columns.Congruency.value] == "incongruent"
        and line[Columns.Block.value] == "Second"
    ):
        return Categories.SocialIncongruentSecondblock

    if (
        line[Columns.Social_Non_Social.value] == "Non-Social"
        and line[Columns.Congruency.value] == "congruent"
        and line[Columns.Block.value] == "First"
    ):
        return Categories.NonSocialCongruentFirstblock

    if (
        line[Columns.Social_Non_Social.value] == "Non-Social"
        and line[Columns.Congruency.value] == "congruent"
        and line[Columns.Block.value] == "Second"
    ):
        return Categories.NonSocialCongruentSecondblock

    if (
        line[Columns.Social_Non_Social.value] == "Non-Social"
        and line[Columns.Congruency.value] == "incongruent"
        and line[Columns.Block.value] == "First"
    ):
        return Categories.NonSocialIncongruentFirstblock

    if (
        line[Columns.Social_Non_Social.value] == "Non-Social"
        and line[Columns.Congruency.value] == "incongruent"
        and line[Columns.Block.value] == "Second"
    ):
        return Categories.NonSocialIncongruentSecondblock



@dataclass
class Average:
    value: float
    trials: int


@dataclass
class Participant:
    id: str
    reaction_time: float
    congruency: bool
    sociality: bool
    block: str
    category: Categories

    @classmethod
    def from_csv_line(cls, csv_line: str) -> "Participant":
        """Create participant from csv line"""
        line = csv_line.split(",")
        return Participant(
            id=line[Columns.ParticipantID.value],
            reaction_time=float(line[Columns.ReactionTime.value]),
            congruency=line[Columns.Congruency.value] == "congruent",
            sociality=line[Columns.Social_Non_Social.value] == "Social",
            block=line[Columns.Block.value],
            category=find_category(line),
        )


def read_file() -> List[str]:
    """Read file for Malika"""
    file = open("Trial RT data_Socoff Simon Task.csv")
    lines: List[str] = file.readlines()
    file.close()
    return lines


def is_correct(csv_line: str):
    line: List[str] = csv_line.split(",")
    return line[Columns.Correct.value] == "1"


def remove_incorrect_answer(lines: List[str]) -> List[str]:
    """Remove lines that have incorrect answer (Column Correct == 0)"""
    csv_lines = lines[1:]
    return list(filter(is_correct, csv_lines))


def map_participants_to_social_first(participants: List[Participant]) -> map:
    """{"participantId": true/false} wether or not social was first"""
    result = {}
    for p in participants:
        if p.id in result:
            continue
        result[p.id] = p.sociality
    return result


def map_participants_to_averages(participants: List[Participant]) -> map:
    """{"participantId": {"category": average }} wether or not social was first"""
    result = {}
    for p in participants:
        if p.id not in result:
            result[p.id] = {}

        averages_for_the_participant = result[p.id]
        category = p.category

        if category not in averages_for_the_participant:
            averages_for_the_participant[category] = Average(p.reaction_time, trials=1)
        # 3 4 5  => 4
        # 3, 1
        # (3 * 1 + 4) / 2 = 3.5
        # (3.5 * 2 + 5) / 3 => 4
        else:
            current_average: Average = averages_for_the_participant[category]
            new_trial = current_average.trials + 1
            averages_for_the_participant[category] = Average(
                value=(current_average.value * current_average.trials + p.reaction_time) / new_trial,
                trials=new_trial
            )
    return result


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
map_of_participants = map_participants_to_social_first(participants)


from pprint import pprint
pprint(correct_trials[:2])
pprint(participants[:2])

averages = map_participants_to_averages(participants)
pprint(averages)
import pdb; pdb.set_trace()
