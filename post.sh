# post local|dev|prod|test|LOG_APP_ENDPOINT NUM_CHARS|STRING
#
# post either a string of '=' of length NUM_CHARS or a custom STRING to
# a log server
#

LOG_APP_ENDPOINT=''
case "$1" in
  local) LOG_APP_ENDPOINT=http://host.docker.internal:5013/dev;;
  dev) LOG_APP_ENDPOINT=$LOG_APP_DEV_ADDRESS/dev;;
  test) LOG_APP_ENDPOINT=$LOG_APP_TEST_ADDRESS/test;;
  prod) LOG_APP_ENDPOINT=$LOG_APP_PROD_ADDRESS/log;;
  *) MODE="$3";;
esac

CHARS=''
re='^[0-9]+$'
if ! [[ $2 =~ $re ]] ; then
   CHARS=$2
else
  
  for i in $(seq 1 $2);
  do
    CHARS=$CHARS=
  done
fi

PROTOCOL=`echo $LOG_APP_ENDPOINT | sed 's/:\/\/.*//'`
ADDRESS=`echo $LOG_APP_ENDPOINT | sed 's/^[^:]*:\/\///'`

# echo $PROTOCOL://$LOG_APP_USERNAME:$LOG_APP_PASSWORD@$ADDRESS
# exit 1
curl -i -X POST -H 'Content-Type: application/json' -d "$CHARS" $PROTOCOL://$LOG_APP_USERNAME:$LOG_APP_PASSWORD@$ADDRESS
