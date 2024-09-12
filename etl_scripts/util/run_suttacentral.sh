#!/bin/bash

# Script to run SuttaCentral setup

make prepare-host
make run-dev-no-logs
make load-data
make index-arangosearch