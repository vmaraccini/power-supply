EXTRA_PARAM=$1

docker pull vmaraccini/ltspice:latest
{ cat "docker-test.sh"; echo " $EXTRA_PARAM" ; } | docker run -i -v "$(pwd)":/mnt/project vmaraccini/ltspice 
