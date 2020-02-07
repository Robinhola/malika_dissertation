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
