#!/bin/bash

#register the package
sudo python3.5 -m pip setup register
#publish a 'downloadble' version
sudo python3.5 -m pip setup sdist upload
