"""
Visualization utilities for scan-to-mesh
"""
from compas_viewer import Viewer
from compas_viewer.config import Config
from compas.geometry import Pointcloud
from compas.datastructures import Mesh
from pathlib import Path

from src import config


def create_viewer(camera_position=None, camera_target=None, camera_scale=None, gridsize=None):
    """
    Create a configured viewer with standard settings.
    
    Args:
        camera_position: Optional custom camera position [x, y, z]
        camera_target: Optional custom camera target [x, y, z]
        camera_scale: Optional custom camera scale
        gridsize: Optional custom grid size (x_size, x_steps, y_size, y_steps)
    
    Returns:
        Viewer: Configured compas_viewer instance
    """
    view_config = Config()
    
    # Set default values if not provided
    view_config.camera.target = camera_target or [0, 0, 0]
    view_config.camera.position = camera_position or [100, -1500, 2000]
    view_config.camera.scale = camera_scale or 100
    view_config.renderer.gridsize = gridsize or (20000, 20, 20000, 20)
    
    return Viewer(config=view_config)


def visualize_pointcloud(viewer, pointcloud=None, filename=None, color=None):
    """
    Add a pointcloud to the viewer.
    
    Args:
        viewer: compas_viewer instance
        pointcloud: Optional Pointcloud object
        filename: Optional path to .ply file
        color: Optional color for the pointcloud
    """
    if pointcloud is None and filename is not None:
        pointcloud = Pointcloud.from_ply(filename)
    
    if pointcloud is not None:
        viewer.scene.add(pointcloud, color=color)


def visualize_mesh(viewer, mesh=None, filename=None, show_points=False, color=None):
    """
    Add a mesh to the viewer.
    
    Args:
        viewer: compas_viewer instance
        mesh: Optional Mesh object
        filename: Optional path to .obj file
        show_points: Whether to show mesh vertices
        color: Optional color for the mesh
    """
    if mesh is None and filename is not None:
        mesh = Mesh.from_obj(filename)
    
    if mesh is not None:
        viewer.scene.add(mesh, show_points=show_points, color=color)


def visualize_combined(pointcloud=True, mesh=True, pointcloud_color=None, mesh_color=None):
    """
    Visualize both pointcloud and mesh in a single viewer.
    
    Args:
        pointcloud: Whether to show pointcloud
        mesh: Whether to show mesh
        pointcloud_color: Optional color for pointcloud
        mesh_color: Optional color for mesh
    """
    viewer = create_viewer()
    
    if pointcloud:
        visualize_pointcloud(
            viewer,
            filename=config.RESULTS_DIR / "pointcloud_origin.ply",
            color=pointcloud_color
        )
    
    if mesh:
        visualize_mesh(
            viewer,
            filename=config.RESULTS_DIR / "mesh.obj",
            show_points=False,
            color=mesh_color
        )
    
    viewer.show() 