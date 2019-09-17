# logdrain

Heroku logdrain

# Quickstart
## Setup
* Install Docker
* `git clone https://github.com/airladon/itiget/`
* Navigate to project directory (all following steps are done from the project directory unless otherwise said)

## Build and deploy to Heroku

```
export HEROKU_API_KEY=`heroku auth:token`
./start_env.sh dev
./build.sh deploy APP-NAME
```

## Using Environment Variables

```
export HEROKU_DEV_ADDRESS=
export HEROKU_TEST_ADDRESS=
export HEROKU_PROD_ADDRESS=
./start_env.sh dev
./build.sh deploy prod
```

## Using `addresses.yml`

Enter dev, test, prod addresses in `addresses.yml`
```
./start_env.sh dev
./build.sh deploy prod
```

## Hooking up to CI

### In Local
Generate a secret key to use in HEROKU (use a different one for each HEROKU repo)
```
python tools/generate_secret_key.py
```

### In Heroku

App->Settings->Reveal Config Vars

Add SECRET_KEY and its value from above

### In Travis
Activate repository on Travis

Add in the heroku addresses of the test and prod apps - e.g. `https://some-app.herokuapp.com`

Pull Requests->Settings

Check only "Build pushed pull requests"

Add Environment Variables:

  * HEROKU_TEST_ADDRESS
  * HEROKU_PROD_ADDRESS
  * HEROKU_API_KEY



### In Github
Github->REPOSITORY_NAME->Settings->Branches->Add Rule

* master
* Require status checks to pass before merging
* Require branches to be up to date before merging
* Include administrators



# Local Development Setup

## Install local Python packages
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

## Run dev container
```
./start_env.sh dev
```
From here, can run pytest, flake8, or flask (flask run --host=0.0.0.0)


## Run dev-server container
```
./start_env.sh dev-server
```

Use a web browser and go to: `http://localhost:5003`


## Run stage container

The stage container runs like production, but runs flask instead of gunicorn so you can see the stage messages.

To access it locally, you need to disable Flask Talisman which forces all communication to https:
```
export LOCAL_PRODUCTION=DISABLE_SECURITY
./start_env.sh stage
```

Use a web browser and go to: `http://localhost:5001`


## Run Prod container

The stage container runs like production, running gunicorn.

To access it locally, you need to disable Flask Talisman which forces all communication to https:
```
export LOCAL_PRODUCTION=DISABLE_SECURITY
./start_env.sh prod
```

Use a web browser and go to: `http://localhost:5000`

NOTE: Do not use HTTPS as it will not work!

