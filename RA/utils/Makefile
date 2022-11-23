

gen:
	echo "Generating protobufs"
	python3 -m grpc_tools.protoc -I generated=../protobufs --python_out=../ --pyi_out=../ --grpc_python_out=../ ../protobufs/*.proto
