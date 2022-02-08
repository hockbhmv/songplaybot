if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/hockbhmv/songplaybot /songplaybot
else
  echo "Cloning $UPSTREAM_REPO branch from Respository"
  git clone https://github.com/hockbhmv/songplaybot -b $UPSTREAM_REPO /songplaybot
fi
cd /songplaybot
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 run.py
