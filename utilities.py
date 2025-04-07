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
