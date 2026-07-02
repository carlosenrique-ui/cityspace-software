from offline.geo.grid_to_temporal_sequence import grid_to_temporal_sequence

def test_grid_to_temporal_sequence():
    pin_heights = {
        (0,0): 0.0,
        (1,0): 5.0,
        (2,0): 10.0,
        (0,1): 2.0,
        (1,1): 4.0,
        (2,1): 6.0,
    }

    seq = grid_to_temporal_sequence(
        pin_heights,
        cols=3,
        rows=2
    )

    for s in seq:
        print(s)

    assert len(seq) == 6
    print("✔ Grid → TemporalSequence OK")

if __name__ == "__main__":
    test_grid_to_temporal_sequence()
