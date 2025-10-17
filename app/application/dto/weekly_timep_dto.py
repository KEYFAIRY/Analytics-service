from dataclasses import dataclass

@dataclass
class WeeklyTimePostureDTO:
    scale: str
    time_practiced: int
    bad_posture_time: int
    good_posture_time: int