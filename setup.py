import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="microprediction",
    version="0.4.0",
    description="Client for www.microprediction.org",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/microprediction",
    author="microprediction",
    author_email="info@microprediction.org",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["microprediction","microprediction.live"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=["numpy","muid","aiohttp","pathlib","retrying","contexttimer","requests"],
    entry_points={
        "console_scripts": [
            "microprediction=microprediction.__main__:main",
        ]
     },
     )
