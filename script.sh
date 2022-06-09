#!/bin/bash
# sudo chmod +x script.sh
clear
echo ""

echo "==> Update main from Git"
git reset --hard
git fetch
git pull
echo ""

echo "==> Update submodules from Git"
git submodule update --remote
echo ""

echo "==> Check and update dependencies"
poetry run poetry update
echo ""

echo "==> Run server"
poetry run main.py
