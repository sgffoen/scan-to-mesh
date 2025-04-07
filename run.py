from pathlib import Path
import numpy as np

from pointcloud import (
    load_point_clouds_from_folder,
    save_pointcloud,
    reconstruction_poisson_surface_reconstruction,
)

from mesh import remesh, save_mesh, slice_mesh_with_base_plane
import config

import compas.geometry as cg
from compas.geometry import Pointcloud
from compas.datastructures import Mesh

from compas_viewer import Viewer
from compas_viewer.config import Config

from compas_cgal.reconstruction import pointset_reduction
from compas_cgal.reconstruction import pointset_outlier_removal



def process_pointclouds():
    # Load all point clouds
    point_clouds = load_point_clouds_from_folder(folder=Path(__file__).parent / "data")
    combined_c = point_clouds[0]
    if len(point_clouds) > 1:
        for c in point_clouds[1:]:
            combined_c.points.extend(c.points)

    pcl = Pointcloud(pointset_reduction(combined_c, 2))
    pcl = Pointcloud(pointset_outlier_removal(pcl, 10, 1.5))
    save_pointcloud(np.array(pcl.points), filename="pointcloud.ply")
    
    return pcl


def create_mesh_from_pointcloud():
    data_dir = Path(__file__).parent / "data" / "results"
    ply_file = data_dir / "pointcloud.ply"
    pointcloud = Pointcloud.from_ply(ply_file)

    points, mesh = reconstruction_poisson_surface_reconstruction(pointcloud)

    tri_remesh = remesh(mesh)

    cut_height = [
        config.SCAN_OBJECT_CENTER_PT.x,
        config.SCAN_OBJECT_CENTER_PT.y,
        config.SCAN_OBJECT_CENTER_PT.z + 20.0,
    ]
    mesh1, mesh2 = slice_mesh_with_base_plane(tri_remesh, cut_plane=cg.Plane(cut_height, [0, 0, 1]))

    data_dir = Path(__file__).parent / "data" / "results"
    obj_file = data_dir / "mesh.obj"
    save_mesh(mesh1, obj_file)

    return mesh1

def view(pointcloud=None, mesh=None):
    data_dir = Path(__file__).parent / "data" / "results"
    if not pointcloud:
        pointcloud = Pointcloud.from_ply(data_dir / "pointcloud.ply")

    if not mesh:
        mesh = Mesh.from_obj(data_dir / "mesh.obj")
    # Visualize the cropped point clouds
    view_config = Config()
    view_config.camera.target = config.SCAN_CENTER_PT
    view_config.camera.position = [100, -1500, 2000]
    view_config.camera.scale = 100
    view_config.renderer.gridsize = (20000, 20, 20000, 20)

    viewer = Viewer(config=view_config)

    viewer.scene.add(pointcloud)
    viewer.scene.add(mesh, show_points=False)

    viewer.show()


if __name__ == "__main__":
    #point_cloud = process_pointclouds()
    #mesh = create_mesh_from_pointcloud()
    view(None, None)