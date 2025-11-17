from datetime import timedelta


# TODO: I want to test this with pytest but using pytest to add unit tests to
# a blender addon is super awkward and I couldn't get it.
def estimate_time_to_completion(
    frame: int,
    max_frame: int,
    avg_time_per_frame: timedelta,
) -> timedelta:
    duration_left: timedelta = (max_frame - frame) * avg_time_per_frame
    return duration_left
