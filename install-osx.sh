#!/bin/bash

# LightTwinSVM Program - Simple and Fast
# Version: 0.1.0-alpha - 2018-05-24
# Developer: Mir, A. (mir-am@hotmail.com)
# License: GNU General Public License v3.0

# In this shell script, required dependencis will be installed.
# for building and testing LightTwinSVM on Travis CI

python --version
echo "OS: $OSTYPE"

if [ "$OSTYPE" == "darwin"* ]
then
	echo "A MacOS system is detected."

else
	echo "OSX not detected!!"
fi
