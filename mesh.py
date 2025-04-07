from compas.datastructures import Mesh
from compas_cgal.meshing import mesh_remesh
from compas_cgal.skeletonization import mesh_skeleton

from slice import mesh_slice_plane

def get_mesh_skeleton(mesh):
    v, f = mesh.to_vertices_and_faces(triangulated=True)

    skeleton_edges = mesh_skeleton((v, f))

    polylines = []
    for start_point, end_point in skeleton_edges:
        polyline = cg.Polyline([start_point, end_point])
        polylines.append(polyline)

    return polylines

def slice_mesh_with_base_plane(mesh, cut_plane):
    result = mesh_slice_plane(mesh, cut_plane)
    return result

def save_mesh(mesh, file_path):
    mesh.to_obj(file_path)
    print(f'Mesh saved to {file_path}')

def remesh(mesh, edge_length=3.0):
    mesh.remove_unused_vertices()

    V0, F0 = mesh.to_vertices_and_faces()
    V1, F1 = mesh_remesh((V0, F0), edge_length, 10)
    remesh = Mesh.from_vertices_and_faces(V1, F1)

    return remesh
