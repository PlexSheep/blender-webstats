from typing import Optional


def log(display):
    """
    Simplest logging ever
    """
    print(f"[WebStats]: {display}")


def log_divider(heading: Optional[str] = None):
    if heading is not None:
        log(f"{heading:=^80}")
    else:
        log("=" * 80)
