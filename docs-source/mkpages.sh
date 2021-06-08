#!/bin/bash

cd "`dirname "$0"`"  # cd to dir of this file

mkdocs build -d ../docs

bash mkapi.sh
