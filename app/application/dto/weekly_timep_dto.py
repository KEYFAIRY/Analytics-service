from dataclasses import dataclass

@dataclass
class WeeklyTimePostureDTO:
    id_student: str
    id_scale: int
    date: str
    year: int
    week: int
    month: int
    time_practiced: int
    bad_posture_time: int
    good_posture_time: int