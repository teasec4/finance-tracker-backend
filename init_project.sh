#!/bin/bash

echo "Создание структуры проекта"

mkdir -p app/{api,models,schemas,db,core}
touch app/__init__.py
touch app/main.py

# Папки с __init__.py
for dir in api models schemas db core
do
    touch app/$dir/__init__.py
done