from setuptools import setup, find_packages

setup(
    name="core",
    version="0.2",
    packages=find_packages(),
    namespace_packages=['plugin'],
    # install_requires=["core>=0.1"],
    # ??
    provides=['plugin.core.services', 'plugin.core', ],
    # entry_points={'web_scripts': ['loader=plugin.loader.']} # TODO ???
    package_data={'core': ['plugin/core/static/*.css', 'plugin/core/static/*.js',
                           'plugin/core/static/*.html', 'plugin/core/templates/*.html']},
    zip_safe=True
)
