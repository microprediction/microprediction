set -e
echo "This script will run DefaultCrawler from a new virtual env"
echo "If it fails you might need to brew install python"
mkdir -p crawling_working_dir
cd crawling_working_dir
python3 -m venv crawling
source crawling/bin/activate
pip install --upgrade wheel
pip install --upgrade pip
pip install --upgrade microprediction
echo "Be sure to grab the write_key and paste it into your dashboard at https://www.microprediction.org"
python3 -c "from microprediction import DefaultCrawler;crawler = DefaultCrawler(difficulty=11); crawler.run()"
