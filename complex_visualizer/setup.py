from setuptools import setup, find_packages

setup(
    name="complex-visualizer",
    author="Anastasija Savic",
    version="0.1",
    packages=find_packages(),
    namespace_packages=["plugin", "plugin.visualizer"],
    entry_points={
        'visualizer':
        ['complex-visualizer=plugin.visualizer.complex_visualizer:ComplexVisualizer']
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)
