from setuptools import setup, find_packages

setup(
    name="core",
    version="0.5",
    packages=find_packages(),
    install_requires=["Django>=2.1"],
    namespace_packages=['plugin'],
    provides=['plugin.core.services', 'plugin.core', ],
    package_data={'core': ['plugin/core/static/*.css', 'plugin/core/static/*.js',
                           'plugin/core/static/*.html', 'plugin/core/templates/*.html']},
    zip_safe=True
)

