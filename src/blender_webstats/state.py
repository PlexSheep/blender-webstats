"""
Render state tracking module.

Provides thread-safe storage for render progress data that can be safely
accessed from both Blender's main thread and the HTTP server thread.
"""

import threading
import time
from typing import Optional, Dict, Any

import bpy.types


class RenderState:
    """
    Thread-safe class for tracking render state and progress.

    This class maintains a copy of render data that can be safely accessed
    from the HTTP server thread without touching Blender's scene objects
    (which are not thread-safe).
    """

    def __init__(self) -> None:
        """Initialize the render state with a lock for thread safety."""
        self._lock: threading.Lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        """Reset all state to initial values."""
        with self._lock:
            self.is_rendering: bool = False
            self.render_start_time: Optional[float] = None
            self.render_complete_time: Optional[float] = None

            # Scene information
            self.scene_name: str = ""
            self.render_engine: str = ""
            self.output_path: str = ""

            # Frame progress
            self.current_frame: int = 0
            self.total_frames: int = 0
            self.frame_start_time: Optional[float] = None

            # Sample progress (Cycles)
            self.current_sample: int = 0
            self.total_samples: int = 0

            # Statistics
            self.render_stats: str = ""
            self.last_update_time: Optional[float] = None

    def get_state(self) -> Dict[str, Any]:
        """
        Return a snapshot of the current state as a dictionary.

        This method is thread-safe and can be called from any thread.

        Returns:
            Dictionary containing all current render state information.
        """
        with self._lock:
            elapsed_time: Optional[float] = None
            estimated_time_remaining: Optional[float] = None

            if self.is_rendering and self.render_start_time is not None:
                elapsed_time = time.time() - self.render_start_time

                # Simple ETA calculation based on frames
                if self.total_frames > 0 and self.current_frame > 0:
                    frames_remaining: int = self.total_frames - self.current_frame + 1
                    time_per_frame: float = elapsed_time / self.current_frame
                    estimated_time_remaining = frames_remaining * time_per_frame

            return {
                "is_rendering": self.is_rendering,
                "scene_name": self.scene_name,
                "render_engine": self.render_engine,
                "output_path": self.output_path,
                "current_frame": self.current_frame,
                "total_frames": self.total_frames,
                "current_sample": self.current_sample,
                "total_samples": self.total_samples,
                "render_stats": self.render_stats,
                "elapsed_time": elapsed_time,
                "estimated_time_remaining": estimated_time_remaining,
                "render_start_time": self.render_start_time,
                "last_update_time": self.last_update_time,
            }

    def update_scene_info(self, scene: bpy.types.Scene) -> None:
        """
        Update scene metadata from Blender scene object.

        Args:
            scene: Blender scene object containing render settings.
        """
        with self._lock:
            self.scene_name = scene.name
            self.render_engine = scene.render.engine
            self.output_path = bpy.path.abspath(scene.render.filepath)
            self.total_frames = scene.frame_end - scene.frame_start + 1

            # Get sample count if using Cycles
            if scene.render.engine == "CYCLES":
                self.total_samples = scene.cycles.samples

    def set_rendering(self, rendering: bool) -> None:
        """
        Set rendering state and update timestamps.

        Args:
            rendering: True if rendering is active, False otherwise.
        """
        with self._lock:
            self.is_rendering = rendering
            current_time: float = time.time()

            if rendering:
                self.render_start_time = current_time
            else:
                self.render_complete_time = current_time

            self.last_update_time = current_time

    def update_frame(self, frame: int) -> None:
        """
        Update current frame being rendered.

        Args:
            frame: Frame number currently being rendered.
        """
        with self._lock:
            self.current_frame = frame
            self.frame_start_time = time.time()
            self.current_sample = 0  # Reset sample count for new frame
            self.last_update_time = time.time()

    def update_sample(self, sample: int) -> None:
        """
        Update current sample progress.

        Args:
            sample: Current sample number being rendered.
        """
        with self._lock:
            self.current_sample = sample
            self.last_update_time = time.time()

    def update_stats(self, stats: str) -> None:
        """
        Update render statistics string.

        Args:
            stats: Statistics string from Blender's render engine.
        """
        with self._lock:
            self.render_stats = stats
            self.last_update_time = time.time()
