cd /Users/pcotton/github/microprediction/
rm /Users/pcotton/github/microprediction/dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
