from pathlib import Path
import numpy as np

import compas.geometry as cg
from compas.datastructures import Mesh
from compas.geometry import Pointcloud

from compas_cgal.reconstruction import pointset_reduction
from compas_cgal.reconstruction import pointset_outlier_removal
from compas_cgal.reconstruction import poisson_surface_reconstruction
from compas_cgal.reconstruction import pointset_normal_estimation

from src.processing.utilities import save_ply
from src import config


def crop_points(points, bbox_min, bbox_max):
    """
    Crop points based on a bounding box.
    
    Args:
        points: numpy array of points (Nx3)
        bbox_min: [x_min, y_min, z_min]
        bbox_max: [x_max, y_max, z_max]
    
    Returns:
        numpy array of cropped points
    """
    # Convert to numpy array if not already
    points = np.array(points)
    
    # Create mask for points within bounding box
    mask = np.all((points >= bbox_min) & (points <= bbox_max), axis=1)
    
    # Return only points that are within the bounding box
    return Pointcloud(points[mask].tolist())

def load_point_clouds_from_folder(folder):
    point_clouds = []
    
    # Read all PLY files from the data directory
    for ply_file in sorted(folder.glob("*.ply")):
        point_cloud = Pointcloud.from_ply(ply_file)
        cropped = crop_points(point_cloud.points, config.BBOX_MIN, config.BBOX_MAX)
        point_clouds.append(cropped)
    
    return point_clouds

def reconstruction_poisson_surface_reconstruction(pointcloud):
    points, normals = pointset_normal_estimation(pointcloud, 7, True)

    V, F = poisson_surface_reconstruction(points, normals)
    mesh = Mesh.from_vertices_and_faces(V, F)

    c = Pointcloud(V)

    return c, mesh

def save_pointcloud(pointcloud, filename="pointcloud.ply"):
    file_path = config.RESULTS_DIR / filename
    save_ply(pointcloud, file_path)
