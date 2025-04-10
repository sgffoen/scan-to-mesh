# config.py
import compas.geometry as cg
from pathlib import Path

POSITIONER_CENTER = [1701.531, -720.42, 881.25]
POSITIONER_CENTER_PT = cg.Point(*POSITIONER_CENTER)
SCAN_OBJECT_HEIGHT = 120.0 #mm

BBOX_SIZE = [500, 500, 800]
BBOX_MIN = list(POSITIONER_CENTER_PT - [BBOX_SIZE[0]/2, BBOX_SIZE[1]/2, -SCAN_OBJECT_HEIGHT])
BBOX_MAX = list(POSITIONER_CENTER_PT + [BBOX_SIZE[0]/2, BBOX_SIZE[1]/2, BBOX_SIZE[2] + SCAN_OBJECT_HEIGHT])

# Update paths to point to the root level data directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = DATA_DIR / "results"
