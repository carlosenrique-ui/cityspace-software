from dataclasses import dataclass

@dataclass
class TimeProfile:
    lift_s: float
    settle_s: float
    hold_s: float
    descend_s: float

    @property
    def total_frame_time(self):
        return (
            self.lift_s +
            self.settle_s +
            self.hold_s +
            self.descend_s
        )
