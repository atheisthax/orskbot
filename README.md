# orskbot

Bot for Telegram channel #orsk
Invite: https://telegram.me/joinchat/B5623z5lC_jsIXaaArVhiA

### Installation
Required python3

Crearte virtualenv
```sh
python -m venv .env
```

Activate virtualenv

Windows
```sh
C:\> .env\Scripts\activate
```

Linux and OS X 
```sh
$ source .env/Scripts/activate
```

Install dependens
```sh
pip install -r requirements.txt
```

### Run

Windows
```sh
bot_loop.cmd
```
or powershell (cmd script won't work fine for me}
```sh
powershell -executionpolicy unrestricted e:\!sys\orskbot\bot_ps.ps1
```

Linux and OS X
```sh
$ source .env/bin/activate
$ python bot.py
```