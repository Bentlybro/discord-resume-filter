import time

from bot.move_tracker import MoveTracker


def test_first_move_allowed():
    tracker = MoveTracker(max_moves=1, window_seconds=300)
    assert tracker.can_move(42)


def test_second_move_blocked_within_window():
    tracker = MoveTracker(max_moves=1, window_seconds=300)
    tracker.record(42)
    assert not tracker.can_move(42)


def test_other_users_unaffected():
    tracker = MoveTracker(max_moves=1, window_seconds=300)
    tracker.record(42)
    assert tracker.can_move(99)


def test_window_expiry_allows_new_move():
    tracker = MoveTracker(max_moves=1, window_seconds=0.05)
    tracker.record(42)
    assert not tracker.can_move(42)
    time.sleep(0.1)
    assert tracker.can_move(42)


def test_higher_quota_respected():
    tracker = MoveTracker(max_moves=3, window_seconds=300)
    tracker.record(42)
    tracker.record(42)
    assert tracker.can_move(42)
    tracker.record(42)
    assert not tracker.can_move(42)
