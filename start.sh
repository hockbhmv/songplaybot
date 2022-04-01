if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/hockbhmv/video-stream /video-stream 
else
  echo "Cloning $UPSTREAM_REPO branch from Respository"
  git clone $UPSTREAM_REPO -b $BRANCH /video-stream
fi
cd /video-stream
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 main.py
