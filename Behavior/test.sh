docker pull vmaraccini/ltspice:latest
echo "Mounting as: $(pwd):/mnt/project"
cat "docker-test.sh" | docker run -i -v "$(pwd)":/mnt/project vmaraccini/ltspice 
