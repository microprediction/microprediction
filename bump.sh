cp /Users/pcotton/github/microprediction-fake-config/config_private.py /Users/pcotton/github/microprediction/microprediction
cd /Users/pcotton/github/microprediction/
rm /Users/pcotton/github/microprediction/dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
cp /Users/pcotton/github/microprediction-real-config/config_private.py /Users/pcotton/github/microprediction/microprediction
