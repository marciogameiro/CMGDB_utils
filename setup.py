import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmgdb_utils",
    version="0.0.1",
    author="Marcio Gameiro",
    author_email="marciogameiro@gmail.com",
    description="CMGDB utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marciogameiro/cmgdb_utils",
    package_dir={'':'src'},
    packages=setuptools.find_packages(),
    install_requires=["CMGDB", "pyCHomP2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
