from setuptools import setup, find_packages

setup(
    name="rdf-loader",
    author="Katarina Vučić",
    version="0.2",
    packages=find_packages(),
    entry_points={
        "loader": 
            ["rdf-loader=plugin.loader.rdf_loader:RdfLoader"]
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)
