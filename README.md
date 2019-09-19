# logdrain

Heroku logdrain

# Quickstart

## Setup Local
* Install Docker
* `git clone https://github.com/airladon/itiget/`

All following steps are done from the project directory in the console unless otherwise said.

Setup environment variables:
```
export HEROKU_API_KEY=
export LOG_APP_DEV_ADDRESS=
export LOG_APP_DEV_NAME=
export LOG_APP_TEST_ADDRESS=
export LOG_APP_TEST_NAME=
export LOG_APP_PROD_ADDRESS=
export LOG_APP_PROD_NAME=
export LOG_STORAGE_ADDRESS=
export LOG_STORAGE_ACCESS_KEY=
export LOG_STORAGE_SECRET_ACCESS_KEY=
export LOG_APP_USERNAME=
export LOG_APP_PASSWORD=
export LOG_AES_KEY=
```

If doing flask tests, or doing a local build/deploy (which will run the flask tests) make sure to set:
```
export LOCAL_PRODUCTION=DISABLE_SECURITY
```

### Create LOCAL logging app
In one console window create the local logging server:
```
unset LOG_STORAGE_ADDRESS
export MAX_LOG_SIZE=100
./start_env.sh dev-server
```

In a different console window POST a string of 101 '=' characters to the server. As the max log size is set to 100, this should trigger an upload of the encrypted log to the local storage.
```
./post.sh local 101
python tools/decrypt.py local_storage/dev/FILE_NAME
```

### Build DEV logging app

```
./start_env.sh
./build.sh deploy dev
```

#### Manual Testing
This will post 1001 '=' characters to the dev logging app. If the MAX_LOG_SIZE is 1000 on the dev logging app, then this should trigger an upload of the encrypted log to the remote log storage. This can then be accessed.
```
./post dev 10001
./get_logs.sh dev latest
./get_logs.sh dev list
./get_logs.sh latest
./get_logs.sh list
./get_logs.sh FILE_NAME
./get_logs.sh dev/
```

#### Hook it up to a HEROKU app as a drain

To add/remove the DEV logging app to be a log drain of a heroku app with name HEROKU_APP_NAME:
```
./drain.sh add HEROKU_APP_NAME dev
./drain.sh remove HEROKU_APP_NAME dev
```


To add/remove the DEV logging app to be a log drain of a heroku app with name HEROKU_APP_NAME:
```
./drain.sh add HEROKU_APP_NAME prod
./drain.sh remove HEROKU_APP_NAME prod
```


## Setup Heroku
Generate a secret key to use in HEROKU (use a different one for each HEROKU repo)
```
python tools/generate_secret_key.py
```

Then, in the heroku web interface:
* Create App
* App->Settings->Reveal Config Vars
* Add SECRET_KEY and its value from above

If you wish to do development and testing on different apps to the production app, then create three apps, and generate a different SECRET_KEY for each:
* APP_NAME-dev
* APP_NAME-test
* APP_NAME-prod


## Build and deploy to Heroku

If you want to build the app and deploy directly to the app APP_NAME on Heroku:

```
export HEROKU_API_KEY=`heroku auth:token`
./start_env.sh dev
./build.sh deploy APP_NAME
```

# Full Setup
Follow Setup Local and Setup Heroku from above.

## Manually deploy with testing:

Setup environment variables in `./containers/dev/addresses.yml` or manually:
```
export LOG_APP_DEV_ADDRESS=
export LOG_APP_TEST_ADDRESS=
export LOG_APP_PROD_ADDRESS=
```

Test endpoints locally:
```
./start_env.sh dev
pytest tests/local
```

Deploy to dev site for experimentation and manual testing:
```
./start_env.sh dev
pytest tests/local
./build.sh deploy dev
```

Deploy to test site and run automated tests
```
./start_env.sh dev
./build.sh deploy test
pytest tests/remote/test tests/remote/common --server test
```

Deploy to prod site and run automated tests
```
./start_env.sh dev
./build.sh deploy prod
pytest tests/remote/test tests/remote/common --server prod
```

OR

After the manual testing, deploy the app automatically through the `deploy_pipeline.sh` script. This will deploy to the test site, do the tests, and then deploy to the prod site and do the tests

```
./start_env.sh dev
./deploy_pipeline.sh
```

## Using Travis to auto deploy
If you clone this repository and use it in another git repository, then you can set up travis to test and deploy the endpoint. The setup below makes it so the `master` branch is protected and can only be updated with a pull request from another branch. Whenever the pull request into `master` is created, Travis will run the `deploy_pipeline.sh` script which will:
* Run lint and automated tests
* Deploy to test server and perform tests
* Deploy to production server and run tests

### In Travis
Activate repository on Travis

Add in the heroku addresses of the test and prod apps - e.g. `https://some-app.herokuapp.com`

Pull Requests->Settings

Check only "Build pushed pull requests"

Add Environment Variables:

  * LOG_APP_TEST_ADDRESS
  * LOG_APP_PROD_ADDRESS
  * HEROKU_API_KEY


### In Github
Github->REPOSITORY_NAME->Settings->Branches->Add Rule

* master
* Require status checks to pass before merging
* Require branches to be up to date before merging
* Include administrators


Later, if you want to clear the variables use:
```
unset HEROKU_API_KEY
unset LOG_APP_DEV_ADDRESS
unset LOG_APP_DEV_NAME
unset LOG_APP_TEST_ADDRESS
unset LOG_APP_TEST_NAME
unset LOG_APP_PROD_ADDRESS
unset LOG_APP_PROD_NAME
unset LOG_STORAGE_ADDRESS
unset LOG_STORAGE_ACCESS_KEY
unset LOG_STORAGE_SECRET_ACCESS_KEY
unset LOG_APP_USERNAME
unset LOG_APP_PASSWORD
unset LOG_AES_KEY
```


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

