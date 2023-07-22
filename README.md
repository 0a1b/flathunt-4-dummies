## Insall:
- install google chrome
- install tmux: ```sudo apt-get install tmux```
- install venv https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
- start virtual environment: source .env/bin/activate
- run in env: ``` pip install -r requirements.txt ``` to install required packages

## usage
 - setup telegram-send with your bot (instructions: https://pypi.org/project/telegram-send/)
 - fill the urls in the script with your search urls
 - start virtual environment: source .env/bin/activate
 - run: ``` tmux attach -t 0 ```
 - execute: ``` sh run.sh ```

The script checks every 2.5 mins for new flats and sends telegram msg if new flats are found.

The script was designed with the german websites. Depending on your language / changes in website design you might need to change the regular expressions used to filter links
