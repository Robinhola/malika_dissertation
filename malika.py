from enum import Enum
from typing import List, Optional
from malika_types import (
    Average,
    Categories,
    Columns,
    Participant,
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
        else:
            # 3 4 5  => 4
            # 3, 1
            # (3 * 1 + 4) / 2 = 3.5
            # (3.5 * 2 + 5) / 3 => 4
            current_average: Average = averages_for_the_participant[category]
            new_trial = current_average.trials + 1
            averages_for_the_participant[category] = Average(
                value=(current_average.value * current_average.trials + p.reaction_time)
                / new_trial,
                trials=new_trial,
            )
    return result


if __name__ == "__main__":
    lines = read_file()
    correct_trials = remove_incorrect_answer(lines)
    participants = [Participant.from_csv_line(csv_line) for csv_line in correct_trials]
    map_of_participants = map_participants_to_social_first(participants)
    map_of_averages = map_participants_to_averages(participants)

    new_file = open("a.out", "w")
    new_file.writelines(
        [
            ",".join(
                [
                    "ParticipantID",
                    *[c.name for c in Categories],
                    "Social/Non-social First",
                ]
            )
            + "\n",
            ",".join(
                [
                    "ParticipantID",
                    *[str(c.value) for c in Categories],
                    "Social/Non-social First",
                ]
            )
            + "\n",
        ]
    )

    new_lines = []
    for participant_id in map_of_participants:
        new_line = [participant_id]
        averages = map_of_averages[participant_id]
        for c in Categories:
            value = averages[c].value
            new_line.append(str(value))
        new_line.append(
            "Social First"
            if map_of_participants[participant_id]
            else "Non-social First"
        )
        new_lines.append(",".join(new_line) + "\n")

    new_file.writelines(new_lines)
    new_file.close()
