from setuptools import setup, find_packages

setup(
    name="rdf-loader",
    author="Katarina Vučić",
    version="0.1",
    packages=find_packages(),
    namespace_packages=["plugin", "plugin.loader"],
    # TODO add entry_points
     entry_points={
        "loader":
        ["rdf-loader=plugin.loader.rdf_loader:RdfLoader"]
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)
