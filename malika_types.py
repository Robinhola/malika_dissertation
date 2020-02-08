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

    @classmethod
    def from_line(cls, line) -> "Categories":
        isSocialCode = 100 if line[Columns.Social_Non_Social.value] == "Social" else 200
        isCongruentCode = 10 if line[Columns.Congruency.value] == "congruent" else 20
        isFirstCode = 1 if line[Columns.Block.value] == "First" else 2
        return cls(isSocialCode + isCongruentCode + isFirstCode)


@dataclass
class Average:
    value: float
    trials: int

    def current_total_values(self):
        return self.value * self.trials


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
            category=Categories.from_line(line),
        )
