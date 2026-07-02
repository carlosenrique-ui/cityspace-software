# online/core/test_calibration.py

from online.core.calibration import (
    GridCalibration,
    PinCalibration,
    CalibrationEngine,
)


def test_calibration_engine():
    grid = GridCalibration(
        z_min_cm=0.0,
        z_max_cm=20.0,
        scale=1.0,
        offset_cm=0.0,
    )

    pins = {
        5: PinCalibration(offset_cm=1.0),
        7: PinCalibration(disabled=True),
    }

    engine = CalibrationEngine(grid, pins)

    assert engine.calibrate(0, 10.0) == 10.0
    assert engine.calibrate(5, 10.0) == 11.0
    assert engine.calibrate(7, 10.0) == 0.0
    assert engine.calibrate(0, 30.0) == 20.0  # saturação

    print("✔ CalibrationEngine OK")


if __name__ == "__main__":
    test_calibration_engine()
