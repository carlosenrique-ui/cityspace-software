# online/time/test_construction_timeline.py

from online.time.construction_timeline import ConstructionTimeline


def main():
    rows, cols = 4, 6

    timeline = ConstructionTimeline(
        rows=rows,
        cols=cols,
        max_height=10.0,
        loop=False,
    )

    # -------------------------------
    # Avanço completo
    # -------------------------------
    for _ in range(rows * cols):
        state = timeline.advance()

    assert state["frame"] == rows * cols
    assert state["grid"].sum() == rows * cols * 10.0

    # -------------------------------
    # Retrocesso completo
    # -------------------------------
    for _ in range(rows * cols):
        state = timeline.reverse()

    assert state["frame"] == 0
    assert state["grid"].sum() == 0.0

    print("✔ ConstructionTimeline OK")


if __name__ == "__main__":
    main()
