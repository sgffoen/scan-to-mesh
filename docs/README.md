# Scan-to-Mesh

A Python tool for converting 3D scans to meshes, with automatic calibration capabilities.

## Project Structure

```
scan-to-mesh/
├── src/                      # Source code
│   ├── calibration/         # Calibration related code
│   │   ├── auto_calibration.py
│   │   └── icp.py
│   ├── geometry/            # Geometry processing
│   │   ├── pointcloud.py
│   │   ├── mesh.py
│   │   └── rhino_geometry.py
│   ├── processing/          # Processing utilities
│   │   ├── slice.py
│   │   ├── utilities.py
│   │   └── visualization.py
│   └── config.py           # Configuration
├── data/                    # Data directory
│   └── icp/                # ICP calibration data
├── tests/                   # Test directory
└── docs/                    # Documentation
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd scan-to-mesh
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Main Pipeline

To run the complete scan-to-mesh pipeline:
```bash
python run.py
```

## Features

- **Point Cloud Processing**
  - Loading and saving point clouds
  - Point cloud reduction and outlier removal
  - Bounding box cropping

- **Mesh Processing**
  - Poisson surface reconstruction
  - Mesh remeshing
  - Mesh slicing
  - Skeleton extraction

- **Calibration**
  - Automatic calibration using ICP
  - Transformation matrix generation and saving

- **Visualization**
  - Interactive 3D visualization
  - Customizable camera settings
  - Combined point cloud and mesh viewing

## Dependencies

- compas>=2.0.0
- compas-cgal>=0.5.0
- compas-viewer>=0.1.0
- numpy>=1.21.0

## Configuration

Configuration settings are stored in `src/config.py`. Key settings include:

- Positioner center coordinates
- Scan object height
- Bounding box dimensions
- Data directory paths

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
