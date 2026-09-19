# Patch SyncedScene to log manim's actual per-call durations, then exec scene_001
import sys
sys.path.insert(0, '.')
import common
from common import SyncedScene, snap

_orig_play_at = SyncedScene.play_at
def play_at(self, t, *anims, run_time=1.0):
    _orig_play_at(self, t, *anims, run_time=run_time)
    actual = self.duration  # set by manim compile/play
    drift = actual - run_time
    if abs(drift) > 1e-9:
        print(f"DRIFT t={t:6.2f} book_rt={run_time:5.2f} actual={actual:7.3f} d={drift:+.3f} :: {type(anims[0]).__name__ if anims else '-'}")
    print(f"CALL t={t:6.2f} rt={run_time:5.2f} actual={actual:7.3f} clock={self._t:7.3f}")
SyncedScene.play_at = play_at

import runpy
sys.argv = ["manim", "--dry_run", "-qh", "scene_001.py", "Scene001", "--media_dir", "../media"]
from manim import __main__ as m  # noqa
runpy.run_module("manim", run_name="__main__")
