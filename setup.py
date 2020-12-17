import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="microprediction",
    version="0.16.2",
    description="Client for www.microprediction.org turnkey community prediction",
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
    packages=["microprediction", "microprediction.live", "microprediction.univariate"],
    test_suite='pytest',
    tests_require=['pytest', 'scipy'],
    include_package_data=True,
    install_requires=["numpy", "pandas", "pathlib", "contexttimer", "requests",
                      "getjson", "microconventions==0.4.6",
                      'pycoingecko', 'apscheduler', 'tdigest','genson','hyperopt',
                      'sklearn','statsmodels'],
    entry_points={
        "console_scripts": [
            "microprediction=microprediction.__main__:main",
        ]
    },
)
