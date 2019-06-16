import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bratsnorm",
    version="0.1",
    author="Christoph Berger",
    author_email="c.berger@tum.de",
    description="A tiny package to normalize BRATS MRI imagery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/christophbrgr/brats_normalize",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux, Mac OS",
    ],
)