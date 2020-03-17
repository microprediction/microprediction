cp /Users/pcotton/github/rediz/README_MICROPREDICTION.md /Users/pcotton/github/microprediction
cd /Users/pcotton/github/microprediction/
rm /Users/pcotton/github/microprediction/dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
