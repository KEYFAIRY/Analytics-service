from dataclasses import dataclass

@dataclass
class WeeklyTimePosture:
    scale: str
    time_practiced: float
    bad_posture_time: float
    good_posture_time: float