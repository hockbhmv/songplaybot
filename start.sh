if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/hockbhmv/songplaybot.git /songplaybot 
  git clone https://github.com/subinps/VCPlayerBot.git /VCPlayerBot  
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /songplaybot
fi
cd /songplaybot
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
