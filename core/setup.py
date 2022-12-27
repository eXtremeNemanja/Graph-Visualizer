from setuptools import setup, find_packages

setup(
    name="json-loader",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['plugin'],
    install_requires=["core>=0.1"],
    package_data={'core': ['plugin/core/static/*.css', 'plugin/core/static/*.js',
                           'plugin/core/static/*.html', 'plugin/core/templates/*.html']},
    zip_safe=True
)
