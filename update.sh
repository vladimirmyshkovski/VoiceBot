git pull
. /var/www/VoiceBot/venv/bin/activate 
pip install -r requirements/base.txt
systemctl restart voicebot.service
systemctl status voicebot.service
