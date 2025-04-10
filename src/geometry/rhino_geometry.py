import Rhino.Geometry as rg

def load_rhino_transform_from_yaml(yaml_path):
    """Load a 4x4 transformation matrix from a YAML file and convert it to a Rhino Transform.

    The YAML file should contain a 4x4 matrix in the following format:
    __version__:
      serializer: 1 
      data: 1
    FloatMatrix:
      Data: [
        [m00, m01, m02, m03],
        [m10, m11, m12, m13],
        [m20, m21, m22, m23],
        [m30, m31, m32, m33],
      ]

    Args:
        yaml_path: Path to the YAML file containing the transformation matrix

    Returns:
        Rhino.Geometry.Transform: A Rhino transform object representing the 4x4 matrix

    Raises:
        ValueError: If the parsed matrix is not 4x4
    """
    
    with open(yaml_path, 'r') as file:
        lines = file.readlines()

    matrix = []
    inside_matrix = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("Data: ["):
            inside_matrix = True
            continue

        if inside_matrix:
            if stripped == "]":
                break  # End of matrix
            # Remove brackets and split into floats
            cleaned = stripped.strip("[],\n ")
            if cleaned:
                values = [float(x.strip()) for x in cleaned.split(",")]
                matrix.append(values)

    if len(matrix) != 4 or any(len(row) != 4 for row in matrix):
        raise ValueError(f"Matrix is not 4x4. Parsed: {matrix}")

    # Build the Rhino Transform
    transform = rg.Transform(1.0)
    for i in range(4):
        for j in range(4):
            transform[i, j] = matrix[i][j]

    return transform
