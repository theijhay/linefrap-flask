#!/bin/bash

echo "👀 Watching for file changes..."

# Use watchmedo to monitor your project
watchmedo shell-command \
    --patterns="*.py;*.html;*.css;*.js" \
    --recursive \
    --command='./deploy.sh' \
    .
