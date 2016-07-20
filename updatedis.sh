#!/bin/bash

#register the package
sudo python3.5 setup.py register
#publish a 'downloadble' version
sudo python3.5 setup.py sdist upload
