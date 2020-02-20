cd /Users/pcotton/github/microprediction/
python setup.py sdist bdist_wheel
rm /Users/pcotton/github/microprediction/dist/*
twine upload dist/*
