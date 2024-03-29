echo "This script will run DefaultCrawler from a new virtual env"
echo "If it fails you might need to brew install python"
mkdir -p crawling_working_dir
cd crawling_working_dir
python3 -m venv crawling
source crawling/bin/activate
pip install --upgrade pip
pip install --upgrade wheel
pip install --upgrade git+https://github.com/microprediction/microprediction.git
pip install --upgrade git+https://github.com/microprediction/muid.git
 
echo "------ Installation complete ------"

WRITE_KEY_FILE="WRITE_KEY.txt"
if [ -f "$WRITE_KEY_FILE" ]
then
   echo "Found "$WRITE_KEY_FILE
else
   echo "Next, burning a write_key which will be your identity. This may take a long time. Go get lunch."
   sleep 10
   echo "Write keys are explained at https://www.microprediction.com/private-keys"
   sleep 10
   echo "Or read the docs https://microprediction.github.io/microprediction/" 
   sleep 10
   echo "Or listen to the first chapter of the book https://github.com/microprediction/building_an_open_ai_network/blob/main/docs/assets/audio/Microprediction_Chapter_1.mp3"
   sleep 10
   echo "By the way until Jan 31, 2023 you can use code MITPHoliday22 at https://www.penguinrandomhouse.com/search/site/?q=9780262047326 for 20 percent off."
   sleep 10
   echo "Or read our blog https://medium.com/@microprediction" 
   sleep 10
   echo "Or view the video tutorials https://microprediction.github.io/microprediction/videos.html"
   sleep 3
   #python3 -c "import os;os.environ['MUID_VERBOSITY']='1';from microprediction import new_key;WRITE_KEY = new_key(difficulty=11);fh = open('WRITE_KEY.txt', 'w');fn.write(WRITE_KEY);fn.close()"
   python3 -c "from microprediction import new_key;WRITE_KEY = new_key(difficulty=11);print(WRITE_KEY)" > WRITE_KEY.txt
fi


sleep 3 
write_key=$(cat "WRITE_KEY.txt")
echo $write_key

START=`date +%s` 
while [ $(( $(date +%s) - 30000000 )) -lt $START ]; do
    write_key=$(cat "WRITE_KEY.txt")
    pip install --upgrade git+https://github.com/microprediction/microprediction.git
    python3 -c "from microprediction import DefaultCrawler;crawler = DefaultCrawler(write_key='"$write_key"',timeout=3600); crawler.run()"
    echo "          -+-             -+-            -+-            "
    echo "                 -+-             -+-            -+-            "
    echo "          -+-             -+-            -+-            "
    echo "Either the crawler crashed, or this is a scheduled upgrade time. Not to worry either way. We shall resume in 20 seconds". 
    sleep 20
done


