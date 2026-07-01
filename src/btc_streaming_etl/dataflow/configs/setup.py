"""Setuptools setup file for packaging Apache Beam dependencies used by the Dataflow pipeline."""

# Imports
# Standard Libaries
import setuptools

# 3rd Party Libraries
# Custom Libraries

PACKAGES = ["apache-beam[gcp]", "apache-beam"]

setuptools.setup(
    name="real_time_btc_streaming_pipeline",
    version="0.1.0",
    setup_requries=PACKAGES,
    install_requires=PACKAGES,
    package=setuptools.find_packages(),
    include_package_data=True,
)
