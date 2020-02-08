from enum import Enum
from typing import Mapping, List, Optional, Tuple
from malika_types import (
    Average,
    Categories,
    Columns,
    Participant,
)

MapParticipantIDToSocialFirst = Mapping[str, bool]
MapCategoryToAverage = Mapping[Categories, Average]
MapParticipantIDToAverages = Mapping[str, MapCategoryToAverage]


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


def map_participants_to_social_first(
    participants: List[Participant],
) -> MapParticipantIDToSocialFirst:
    """{"participantId": true/false} wether or not social was first"""
    result = {}
    for p in participants:
        if p.id in result:
            continue
        result[p.id] = p.sociality
    return result


def map_participants_to_averages(
    participants: List[Participant],
) -> MapParticipantIDToAverages:
    """{"participantId": {"category": average }} wether or not social was first"""
    map_participant_id_to_average = {}

    for p in participants:
        if p.id not in map_participant_id_to_average:
            map_participant_id_to_average[p.id] = {}

        averages_for_the_participant = map_participant_id_to_average[p.id]
        category = p.category

        if category not in averages_for_the_participant:
            averages_for_the_participant[category] = Average(value=0, trials=0)

        current_average: Average = averages_for_the_participant[category]
        new_total_values = current_average.current_total_values() + p.reaction_time
        number_of_trials = current_average.trials + 1

        averages_for_the_participant[category] = Average(
            value=new_total_values / number_of_trials, trials=number_of_trials,
        )

    return map_participant_id_to_average


def parse_file() -> Tuple[MapParticipantIDToSocialFirst, MapParticipantIDToAverages]:
    lines = read_file()
    correct_trials = remove_incorrect_answer(lines)
    participants = [Participant.from_csv_line(csv_line) for csv_line in correct_trials]
    map_of_participants = map_participants_to_social_first(participants)
    map_of_averages = map_participants_to_averages(participants)
    return (map_of_participants, map_of_averages)


def make_column_names(file) -> List[str]:
    first_column = "ParticipantID"
    category_names = [c.name for c in Categories]
    category_codes = [str(c.value) for c in Categories]
    last_column = "Social/Non-social First\n"

    first_row = ",".join([first_column, *category_names, last_column])
    second_row = ",".join([first_column, *category_codes, last_column])

    return [first_row, second_row]


def make_participant_lines(
    map_participants_social_first: MapParticipantIDToSocialFirst,
    map_participants_averages: MapParticipantIDToAverages,
) -> List[str]:
    new_lines = []

    for participant_id in map_participants_social_first:
        new_line = [participant_id]

        averages = map_participants_averages[participant_id]
        for c in Categories:
            value = averages[c].value
            new_line.append(str(value))

        new_line.append(
            "Social First"
            if map_participants_social_first[participant_id]
            else "Non-social First"
        )

        new_lines.append(",".join(new_line) + "\n")

    return new_lines
