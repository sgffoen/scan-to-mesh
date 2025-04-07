from compas.geometry import icp_numpy
from compas.geometry import Pointcloud
from pointcloud import crop_points

from compas_cgal.reconstruction import pointset_reduction
from compas_cgal.reconstruction import pointset_outlier_removal

from pathlib import Path
import config

from compas_viewer import Viewer
from compas_viewer.config import Config


data_dir = Path(__file__).parent / "data" / "icp"
source_pcl = Pointcloud.from_ply(data_dir / "pcl_0.ply")
target_pcl = Pointcloud.from_ply(data_dir / "pcl_1.ply")

src_pcl_crop = crop_points(source_pcl.points, config.BBOX_MIN, config.BBOX_MAX)
target_pcl_crop = crop_points(target_pcl.points, config.BBOX_MIN, config.BBOX_MAX)

pcl_src = Pointcloud(pointset_reduction(src_pcl_crop , 2))
pcl_src = Pointcloud(pointset_outlier_removal(pcl_src, 10, 1.5))
pcl_target = Pointcloud(pointset_reduction(target_pcl_crop, 2))
pcl_target = Pointcloud(pointset_outlier_removal(pcl_target, 10, 1.5))

source = Pointcloud(pointset_reduction(pcl_src, 10))
target = Pointcloud(pointset_reduction(pcl_target, 10))

points_transformed, T = icp_numpy(source, target)

trans_pcl = source.copy()
trans_pcl.points = points_transformed.tolist()

print(T)

view_config = Config()
view_config.camera.target = config.SCAN_CENTER_PT
view_config.camera.position = [100, -1500, 2000]
view_config.camera.scale = 100
view_config.renderer.gridsize = (20000, 20, 20000, 20)

viewer = Viewer(config=view_config)

viewer.scene.add(source)
viewer.scene.add(target)
viewer.scene.add(trans_pcl)


viewer.show()