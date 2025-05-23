"""
Auto calibration module for scan-to-mesh
"""
import sys
from pathlib import Path

# Add project root to Python path when running this file directly
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.append(str(project_root))

from compas.geometry import icp_numpy
from compas.geometry import Pointcloud
from src.geometry.pointcloud import crop_points
from compas_cgal.reconstruction import pointset_reduction
from compas_cgal.reconstruction import pointset_outlier_removal
from pathlib import Path
import src.config as config
from src.calibration.icp import icp_numpy_no_pca
from src.processing.utilities import transformation_matrix_to_yaml
from compas.tolerance import TOL
import src.processing.visualization as vis



def load_and_preprocess_pointclouds(data_dir):
    """Load and preprocess the point clouds for ICP registration."""
    target_pcl = Pointcloud.from_ply(data_dir / "pointcloud_origin.ply")
    src_pcl = target_pcl.rotated(angle=0.9, axis=[0, 0, 1])
    
    # Reduce point set density for faster processing
    source = Pointcloud(pointset_reduction(src_pcl, 10))
    target = Pointcloud(pointset_reduction(target_pcl, 10))
    
    return source, target


def perform_icp_registration(source, target):
    """Perform ICP registration between source and target point clouds."""
    points_transformed, transformation_matrix = icp_numpy_no_pca(
        source, 
        target, 
        TOL.approximation, 
        maxiter=200
    )
    
    # Create transformed point cloud
    trans_pcl = source.copy()
    trans_pcl.points = points_transformed.tolist()
    
    return trans_pcl, transformation_matrix


def save_transformation_matrix(transformation_matrix, output_path):
    """Save the transformation matrix to a YAML file."""
    transformation_matrix_to_yaml(transformation_matrix, output_path)


def visualize_results(viewer, source, target, transformed):
    """Visualize the point clouds in the viewer."""
    viewer.scene.add(source)
    viewer.scene.add(target)
    viewer.scene.add(transformed)
    viewer.show()


def main():
    # Set up paths
    data_dir = config.DATA_DIR / "icp"
    
    # Load and preprocess point clouds
    source, target = load_and_preprocess_pointclouds(data_dir)
    
    # Perform ICP registration
    transformed_pcl, transformation_matrix = perform_icp_registration(source, target)
    
    # Print and save results
    print(transformation_matrix)
    save_transformation_matrix(transformation_matrix, data_dir / "transformation_matrix.yaml")
    
    # Visualize results
    viewer = vis.create_viewer()
    visualize_results(viewer, source, target, transformed_pcl)


if __name__ == "__main__":
    main()