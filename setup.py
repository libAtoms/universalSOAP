import setuptools

setuptools.setup(
    name="universalSOAP",
    version="0.1.0b",
    packages=setuptools.find_packages(exclude=["tests"]),
    entry_points="""
    [console_scripts]
    universalSOAP_descriptors=universalSOAP.cli.write_descriptor_quantities:main
    """
)
