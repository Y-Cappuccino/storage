#!/usr/bin/env bash

python -m venv .venv
. .venv/bin/activate
pip install pybuilder
pip install twine
pip install --index-url https://yaiba:Danst0ncu1%21@nexus.ycappuccino.fr/ ycappuccino_core
pyb publish
if [ -z "$1" ]
then
    echo "No username supplied"
    exit 0
fi
if [ -z "$2" ]
then
    echo "No password supplied"
    exit 0
fi
twine upload  target/dist/ycappuccino_core*/dist/ycappuccino_storage*.whl --repository-url https://nexus.ycappuccino.fr/ -u$1 -p$2