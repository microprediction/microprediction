mkdir crawling_working_dir
cd crawling_working_dir
python3 -m venv crawling
source crawling/bin/activate
pip install --upgrade microprediction
python3 -c "from microprediction import DefaultCrawler;crawler = DefaultCrawler(); crawler.run()"