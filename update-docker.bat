docker build . --tag pythonagend:latest
docker tag pythonagend:latest okramer170487/privatdockerhub:pythonagend
docker push okramer170487/privatdockerhub:pythonagend