# runs SD API, SD RPC simultaneously:
#export PYTHONENV=${PYTHONENV}:/home/iot/IoT/SD

#env

python3 ./api/server.py  # HTTP Rest (API) Server
#P1=$!
#python3 ./services/SD.py & # gRPC Server
#P2=$!
#wait $P1 $P2
#wait $P1
