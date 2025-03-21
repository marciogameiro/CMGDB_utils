import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CMGDB_utils",
    version="1.0.0",
    author="Marcio Gameiro",
    author_email="marciogameiro@gmail.com",
    description="CMGDB utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marciogameiro/CMGDB_utils",
    package_dir={'':'src'},
    packages=['CMGDB_utils'],
    install_requires=["DSGRN", "pyCHomP2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
