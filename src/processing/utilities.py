def save_ply(points, filename):
    """
    Save a point cloud to a PLY file (ASCII format).
    - points: Nx3 array-like
    """
    num_points = len(points)

    header = [
        "ply",
        "format ascii 1.0",
        f"element vertex {num_points}",
        "property float x",
        "property float y",
        "property float z",
        "end_header"
    ]

    with open(filename, 'w') as f:
        f.write('\n'.join(header) + '\n')
        for pt in points:
            f.write(f"{pt[0]} {pt[1]} {pt[2]}\n")

    print("Pointcloud saved")


def transformation_matrix_to_yaml(matrix, file_path, version_serializer=1, version_data=1, float_precision=9):
    """
    Save a 4x4 transformation matrix as a YAML file in a structured format.

    Parameters:
    - matrix: 4x4 array-like (e.g. NumPy array or nested list)
    - file_path: str, path to the output .yaml file
    - version_serializer: int, version number for the serializer field
    - version_data: int, version number for the data field
    - float_precision: int, number of decimal places for floats
    """
    yaml_content = (
        "__version__:\n"
        f"  serializer: {version_serializer}\n"
        f"  data: {version_data}\n"
        "FloatMatrix:\n"
        "  Data: [\n"
    )

    for row in matrix:
        formatted_row = ", ".join(f"{val:.{float_precision}f}" for val in row)
        yaml_content += f"    [{formatted_row}],\n"

    yaml_content += "  ]\n"

    with open(file_path, 'w') as file:
        file.write(yaml_content)