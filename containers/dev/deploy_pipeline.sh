#!/bin/bash

# Setup colors and text formatting
red=`tput setaf 1`
green=`tput setaf 2`
cyan=`tput setaf 6`
yellow=`tput setaf 3`
bold=`tput bold`
reset=`tput sgr0`

PROJECT_PATH=`pwd`

check_status() {
  if [ $? != 0 ];
  then
    echo
    echo "${bold}${red}Build failed${reset}"
    echo
    exit 1
  else
    echo "${bold}${green}OK${reset}"
  fi
}

title() {
    echo
    echo "${bold}${cyan}=================== $1 ===================${reset}"
}

# From https://github.com/travis-ci/travis-ci/issues/4704 to fix an issue 
# where Travis errors out if too much information goes on stdout and some
# npm package is blocking stdout.
python -c 'import os,sys,fcntl; flags = fcntl.fcntl(sys.stdout, fcntl.F_GETFL); fcntl.fcntl(sys.stdout, fcntl.F_SETFL, flags&~os.O_NONBLOCK);'


###########################################################################
title "Run Lint and Local Tests"
./build.sh prod
check_status

###########################################################################
title "Deploy to thisiget-log-test"
./build.sh deploy test skip-tests skip-build
check_status

title "Delay for thisiget-test to restart"
sleep 5s
check_status

# # Run Deploy Tests here
# check_status

###########################################################################
CURRENT_VERSION=`heroku releases -a thisiget | sed -n '1p' | sed 's/^.*: //'`
title "Deploy to thisiget - current: $CURRENT_VERSION"
./build.sh deploy thisiget-log skip-tests skip-build
check_status

title "Delay for thisiget to restart"
sleep 5s
check_status

# # Run Prod Tests here and Rollback if fail
if [ $? != 0 ];
then
    heroku rollback $CURRENT_VERSION
    NEW_VERSION=`heroku releases -a thisiget | sed -n '1p' | sed 's/^.*: //'`
    echo "${red}${bold}Production deployment failed${reset}"
    if [ "$NEW_VERSION" = "$CURRENT_VERSION" ];
    then
        echo "${red}${bold}Rolled back to $CURRENT_VERSION${reset}"
        echo
    else
        echo "${red}${bold}Rollback to $CURRENT_VERSION failed${reset}"
        echo
    fi
    exit 1
fi

