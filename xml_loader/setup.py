from setuptools import setup, find_packages

setup(
    name="xml-loader",
    # TODO add author
    author="Nemanja Dutina",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['plugin'],
    # TODO add entry_points
    entry_points={
        'loader':
        ['xml-loader=plugin.loader.xml_loader:XmlLoader']
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)
