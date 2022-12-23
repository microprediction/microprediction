import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="microprediction",
    version="1.1.25",
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
        "Programming Language :: Python :: 3.8",
    ],
    packages=["microprediction", "microprediction.live", "microprediction.inclusion","microprediction.univariate", "microprediction.bespoke",
              "microprediction.bespoke.meme_stocks","microprediction.bespoke.golf","microprediction.bespoke.crypto"],
    test_suite='pytest',
    tests_require=['pytest', 'scipy'],
    include_package_data=True,
    install_requires=["numpy>=1.20.1", "pandas", "contexttimer", "requests",
                      "getjson>=2.0.0", "microconventions>=1.0.0","pytz>=2021.3",
                      'pycoingecko', 'tdigest','genson','hyperopt',
                      'scikit-learn','statsmodels','copulas'],
    entry_points={
        "console_scripts": [
            "microprediction=microprediction.__main__:main",
        ]
    },
)
