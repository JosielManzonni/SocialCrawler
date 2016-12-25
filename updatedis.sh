#!/bin/bash

#register the package
sudo python3 setup.py register
#publish a 'downloadble' version
sudo python3 setup.py sdist bdist_wheel

twine upload dist/*

