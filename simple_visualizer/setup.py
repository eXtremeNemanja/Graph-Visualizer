from setuptools import setup, find_packages

setup(
    name="simple-visualizer",
    author="Hristina Adamović",
    version="0.2",
    packages=find_packages(),
    namespace_packages=['plugin'],
    entry_points={
        'visualizer':
        ['simple-visualizer=plugin.visualizer.simple_visualizer:SimpleVisualizer']
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)
