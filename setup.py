import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slave",
    version="0.0.2",
    author="Diego Rodrigues",
    author_email="di3go.r0drigues@gmail.com",
    description="A slave package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/Naine/slave/src/master/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)