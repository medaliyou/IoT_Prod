# runs SD API, SD RPC simultaneously:

python3 ./api/server.py & # HTTP Rest (API) Server
P1=$!
python3 ./services/MU.py & # gRPC Server
P2=$!
wait $P1 $P2