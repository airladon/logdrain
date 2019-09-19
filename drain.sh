# drain add HEROKU_APP dev|prod|test|LOG_APP_ENDPOINT
# drain remove HEROKU_APP dev|prod|test|LOG_APP_ENDPOINT

ACTION=add

if [ "$1" = "remove" ] || [ "$1" = "rm" ];
then
  ACTION=remove
fi

LOG_APP_ENDPOINT=''
case "$3" in
  dev) LOG_APP_ENDPOINT=$LOG_APP_DEV_NAME/dev;;
  test) LOG_APP_ENDPOINT=$LOG_APP_TEST_NAME/test;;
  prod) LOG_APP_ENDPOINT=$LOG_APP_PROD_NAME/log;;
  *) MODE="$3";;
esac

heroku drains:$ACTION https://$LOG_APP_USERNAME:$LOG_APP_PASSWORD@$LOG_APP_ENDPOINT -a $2
