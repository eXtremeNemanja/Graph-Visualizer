from setuptools import setup, find_packages

setup(
    name="xml-loader",
    author="Nemanja Dutina",
    version="0.2",
    packages=find_packages(),
    namespace_packages=['plugin'],
    entry_points={
        'loader': 
        ['xml-loader=plugin.loader.xml_loader:XmlLoader']
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)
