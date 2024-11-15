#! /usr/bin/bash
path=$(pwd)
exportstring='export PATH="$PATH:'
exportstring+=$path
exportstring+='"'
echo $exportstring >> ~/.bashrc
