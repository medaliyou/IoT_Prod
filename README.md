# This repository is a Proof of Concept (PoC) implementation for the article   
## A Secure and Lightweight Authentication Protocol for IoT-Based Smart Homes [link](https://www.mdpi.com/1424-8220/21/4/1488/htm)  

### Global structure
For each **entity**:
 - Smart Device
 - Mobile User
 - Registration Authority
 - Home Gateway

and for the **client**
 - Mobile Phone

There corresponds a folder containing the project files.  

The following mapping describes each entity's folder and the used technology:  

 1. [x] Smart Device `SD` ( **Python3 + gRPC** )  
 2. [x] Mobile User `MU` ( **Python3 + gRPC** )  
 3. [x] Registration Authority `RA` ( **Python3 + gRPC** )  
 4. [x] Home Gateway `HGW` ( **Python3 + gRPC** )  
 5. [x] Mobile Phone `SPA` ( **React** )  




### Project structure


Inside each entity's project folder, we find the following structure:  

| File/Folder | Comment |
|--|--|
| core | Entity's mathematical operations  |
| api | HTTP REST API endpoints for **client** interaction   |
| database | Object for interaction with database (saving/lolading context)  |
| protobufs | Google's gRPC protocl buffers defintion files |
| services | gRPC IPC server  |
| stubs | gRPC IPC client  |
| generated | gRPC protobuf compiled files |
| common | common python modules |
| config | environnent configuration module |
| Dockerfile | Dockerfile |
| .dockerignore | docker ignore |
| .env   | environnement variables  |
| requirements.txt | Python requirements  |

