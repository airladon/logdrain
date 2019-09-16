# logdrain

Heroku logdrain

## Setup
* Install Docker
* `git clone https://github.com/airladon/itiget/`
* Navigate to project directory (all following steps are done from the project directory unless otherwise said)

## Install local Python and Node packages
Local packages for python and node can be used by editors for lint and type hints, as well as allows flask database management.

In addition, python is required for some scripts in the `tools` folder.

### Install Python and Packages
#### Install PyEnv and Python 3.7.1 (if not already installed on local machine)
* Install pyenv
  * `brew install pyenv`
* Add pyenv to shell rc file
  * `echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc`
* Run shell rc file to take effect
  * `source ~/.zshrc`
* Install python version of interest
  * `pyenv install 3.7.1`
* Set python version as default if wanted (but not needed)
* `pyenv global 3.7.1 3.6.6 2.7.14 system`

>> If pyenv install doesn't work because of zlib failure, do this:
`xcode-select --install`

>> If it still doesn't work, then do this
`sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /`

#### Setup and Start Python Virtual environment
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
