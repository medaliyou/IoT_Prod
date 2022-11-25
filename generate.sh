#!/bin/bash

PARENT=$(pwd)
echo "Generating HGW"
cd HGW/utils && make gen

cd $PARENT
echo "Generating RA"
cd  RA/utils && make gen

cd $PARENT
echo "Generating SD"
cd  SD/utils && make gen

cd $PARENT
echo "Generating MU"
cd  MU/utils && make gen

echo "Done!"