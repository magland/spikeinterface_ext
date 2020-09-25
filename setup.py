import setuptools

d = {}
exec(open("spikeinterface_ext/version.py").read(), None, d)
version = d['version']
pkg_name = "spikeinterface_ext"
long_description = open("README.md").read()

setuptools.setup(
    name=pkg_name,
    version=version,
    description="Additional objects for SpikeForest project",
    url="https://github.com/SpikeInterface/spikeinterface_ext",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={},
    install_requires=[
        'numpy',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    )
)
