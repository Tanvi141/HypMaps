import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hyp-maps", 
    version="0.0.1",
    author="Tanvi Karandikar",
    author_email="tanvi.karandikar141@gmail.com",
    description="A small package to transform points between spaces ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tanvi141/HypMaps",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
	install_requires=['numpy'],
)
