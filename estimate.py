from datetime import timedelta


def estimate_time_to_completion(
    frame: int,
    max_frame: int,
    avg_time_per_frame: timedelta,
) -> timedelta:
    duration_left: timedelta = (max_frame - frame) * avg_time_per_frame
    return duration_left
