# config.py
import compas.geometry as cg

SCAN_CENTER_PT = [1701.531, -720.42, 651]
SCAN_OBJECT_CENTER_PT = cg.Point(*SCAN_CENTER_PT)

BBOX_SIZE = [500, 500, 500]
BBOX_MIN = list(SCAN_OBJECT_CENTER_PT - [BBOX_SIZE[0]/2, BBOX_SIZE[1]/2, 0])
BBOX_MAX = list(SCAN_OBJECT_CENTER_PT + [BBOX_SIZE[0]/2, BBOX_SIZE[1]/2, BBOX_SIZE[2]])