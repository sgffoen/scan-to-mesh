from pathlib import Path
import numpy as np

from src.geometry.pointcloud import (
    load_point_clouds_from_folder,
    save_pointcloud,
    reconstruction_poisson_surface_reconstruction,
)

from src.geometry.mesh import remesh, save_mesh, slice_mesh_with_base_plane
from src import config
from src.processing.visualization import visualize_combined

import compas.geometry as cg
from compas.geometry import Pointcloud
from compas.datastructures import Mesh

from compas_viewer import Viewer
from compas_viewer.config import Config

from compas_cgal.reconstruction import pointset_reduction
from compas_cgal.reconstruction import pointset_outlier_removal



def process_multiple_scans_to_pointcloud():
    # Load all point clouds
    point_clouds = load_point_clouds_from_folder(folder=config.DATA_DIR)
    combined_c = point_clouds[0]
    if len(point_clouds) > 1:
        for c in point_clouds[1:]:
            combined_c.points.extend(c.points)

    pcl = Pointcloud(pointset_reduction(combined_c, 2))
    pcl = Pointcloud(pointset_outlier_removal(pcl, 10, 1.5))
    save_pointcloud(np.array(pcl.points), filename="pointcloud.ply")

    pcl_transformed = pointcloud_translation_to_origin(pcl)
    
    return pcl_transformed


def pointcloud_translation_to_origin(pointcloud):
    ply_file = config.RESULTS_DIR / "pointcloud.ply"
    pointcloud = Pointcloud.from_ply(ply_file)

    T = cg.Point(0,0,0) - config.POSITIONER_CENTER_PT
    
    tranformed_pointcloud = pointcloud.translated(T)

    save_pointcloud(np.array(tranformed_pointcloud.points), filename="pointcloud_origin.ply")

    return tranformed_pointcloud 


def create_mesh_from_pointcloud():
    ply_file = config.RESULTS_DIR / "pointcloud_origin.ply"
    pointcloud = Pointcloud.from_ply(ply_file)

    points, mesh = reconstruction_poisson_surface_reconstruction(pointcloud)

    tri_remesh = remesh(mesh)

    cut_height = [0, 0, config.SCAN_OBJECT_HEIGHT]
    mesh1, mesh2 = slice_mesh_with_base_plane(tri_remesh, cut_plane=cg.Plane(cut_height, [0, 0, 1]))

    obj_file = config.RESULTS_DIR / "mesh.obj"
    save_mesh(mesh1, obj_file)

    return mesh1

def view(pointcloud=True, mesh=True):
    """Visualize the results using the visualization utilities."""
    visualize_combined(pointcloud=pointcloud, mesh=mesh)


if __name__ == "__main__":
    #point_cloud = process_multiple_scans_to_pointcloud()
    mesh = create_mesh_from_pointcloud()
    view(pointcloud=True, mesh=True)