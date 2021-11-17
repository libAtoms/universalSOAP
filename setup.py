import setuptools

setuptools.setup(
    name="universalSOAP",
    version="0.1.0b",
    packages=["universalSOAP"],
    entry_points="""
    [console_scripts]
    universalSOAP_descriptors=universalSOAP.cli.write_descriptor_quantities:main
    """
)
