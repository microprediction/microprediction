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
 
echo "------ Installation complete ------"
echo "Next, burning a write_key which will be your identity. This may take a long time."
sleep 3

# Make a write key
python3 -c "from microprediction import new_key;WRITE_KEY = new_key();print(WRITE_KEY)" > "WRITE_KEY.txt"

sleep 3 
source "WRITE_KEY.txt"
write_key=$(cat "$file")
echo $write_key


START=`date +%s` 
while [ $(( $(date +%s) - 30000000 )) -lt $START ]; do
    set -e
    . /home/me/.virtualenvs/micro/bin/activate
    pip install git+git://github.com/microprediction/microprediction.git
    python3 -c "from microprediction import DefaultCrawler;crawler = DefaultCrawler(write_key=$write_key); crawler.run()"
    sleep 60
done


