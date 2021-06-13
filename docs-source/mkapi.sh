#!/bin/bash

cd "`dirname "$0"`"  # cd to dir of this file

pydoctor --make-html \
         --html-output=../docs/api \
         --docformat=restructuredtext \
         --project-name="gtgrid" \
         --project-version="1.0.0-beta.2" \
         --project-url=https://devlog42.github.io/qtgrid/ \
         ../qtgrid/
