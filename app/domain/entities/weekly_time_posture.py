from dataclasses import dataclass

@dataclass
class WeeklyTimePosture:
    id_student: str
    id_scale: int
    date: str
    year: int
    week: int
    month: int
    time_practice: float
    bad_posture_time: float
    good_posture_time: float