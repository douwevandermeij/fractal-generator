from setuptools import find_packages, setup

REQUIREMENTS = (
    # "fractal",
    "dill",
    "jinja2",
)
TEST_REQUIREMENTS = (
    "black",
    "flake8",
    "isort",
)


setup(
    name="fractal-generator",
    version="0.0.1",
    author="Douwe van der Meij",
    author_email="douwe@karibu-online.nl",
    description="""Fractal-generator is a code generator for projects using Fractal.
    """,
    long_description=open("README.md", "rt").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/douwevandermeij/fractal-generator",
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
    ],
)
