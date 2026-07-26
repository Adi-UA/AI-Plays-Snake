from gamesrc.constants import GRID_SIZE
from gamesrc.grid import Grid


def test_new_grid_is_entirely_free():
    grid = Grid()
    assert all(
        grid.get_status(x, y) == 1
        for y in range(GRID_SIZE)
        for x in range(GRID_SIZE)
    )


def test_update_pos_marks_a_cell_occupied():
    grid = Grid()
    grid.update_pos(5, 5, 1)
    assert grid.get_status(5, 5) == 0


def test_remove_pos_frees_a_cell():
    grid = Grid()
    grid.update_pos(5, 5, 1)
    grid.remove_pos(5, 5)
    assert grid.get_status(5, 5) == 1


def test_out_of_bounds_cells_are_always_blocked():
    assert Grid().get_status(-1, 0) == 0
    assert Grid().get_status(GRID_SIZE, 0) == 0
    assert Grid().get_status(0, -1) == 0
    assert Grid().get_status(0, GRID_SIZE) == 0
