docker pull vmaraccini/ltspice:latest
cat "docker-test.sh" | docker run -i -v "$(pwd)":/mnt/project vmaraccini/ltspice 
