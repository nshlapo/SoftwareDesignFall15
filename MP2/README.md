#Computational Art Project

This project uses nested lists and recursive functions to create randomly generated stills and videos.

##Required Packages
####PIL
sudo pip install pillow
####ffmpeg
######This is not an official package in Ubuntu 14, so you need to add the following repository:

sudo add-apt-repository 'deb http://ppa.launchpad.net/jon-severinsson/ffmpeg/ubuntu '"$(cat /etc/*-release | grep "DISTRIB_CODENAME=" | cut -d "=" -f2)"' main' && sudo apt-get update
######Then:
sudo apt-get install ffmpeg
