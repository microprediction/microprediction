mkdir mining_working_dir
cd mining_working_dir
python3 -m venv miningenv
source miningenv/bin/activate
pip install --upgrade microprediction
echo "Plese enter the donation password. (Ask peter for it)"
read -p 'password: ' PASSWORD
echo "How would you like to be identified?"
read -p 'donor: ' DONOR
python3 -c "import microprediction;microprediction.donate(password='$PASSWORD',donor='$DONOR')"