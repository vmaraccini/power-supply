EXTRA_PARAM=${1:-"discover -s Tests"}

echo "Running tests with arguments: $EXTRA_PARAM"
docker pull vmaraccini/ltspice:latest
{ cat "docker-test.sh"; echo " $EXTRA_PARAM" ; } | docker run -i -v "$(pwd)":/mnt/project vmaraccini/ltspice 
