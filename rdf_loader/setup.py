from setuptools import setup, find_packages

setup(
    name="rdf-loader",
    author="Katarina Vučić",
    version="0.2",
    packages=find_packages(),
    namespace_packages=['plugin'],
    entry_points={
        "loader": 
            ["rdf-loader=plugin.loader.rdf_loader:RdfLoader"]
    },
    install_requires=["core>=0.1", "rdflib"],
    zip_safe=True
)
