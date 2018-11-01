
echo 'Setting up Docker Container, this may take a while'

cd fuzzingbook-dockerenv
docker build -t 'fuzzing-book' --force-rm=true .

echo 'Execute run_docker.sh to start a local server with the interactive notebook'