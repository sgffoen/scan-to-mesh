from setuptools import setup, find_packages

setup(
    name="scan-to-mesh",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "compas>=2.0.0",
        "compas-cgal>=0.5.0",
        "compas-viewer>=0.1.0",
        "numpy>=1.21.0",
    ],
    author="Simon Griffioen",
    author_email="s.griffioen@hva.nl",
    description="A tool for converting 3D scans to meshes",
    long_description=open("docs/README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
) 