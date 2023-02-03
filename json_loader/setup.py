from setuptools import setup, find_packages

setup(
    name="json-loader",
    author="Milica Sladakovic",
    version="0.4",
    packages=find_packages(),
    namespace_packages=['plugin'],
    entry_points={
        "loader": 
        ["json-loader=plugin.loader.json_loader:JsonLoader"]
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)
