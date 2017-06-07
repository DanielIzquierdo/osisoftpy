#!/usr/bin/env bash

# install dev dependencies
python setup.py develop
pip-compile dev-requirements.in -o requirements/dev.txt --upgrade
pip-compile test-requirements.in -o requirements/test.txt --upgrade
pip-compile setup.py -o requirements/prod.txt --upgrade
pip install -r dev-requirements.txt
pip install -r test-requirements.txt
pip install -r requirements.txt
pip-sync dev-requirements.txt requirements.txt
# add colors to nosetests
pip install rednose

# clean ./build
python setup.py clean --all
python setup.py sdist
python setup.py bdist_wheel
pip install dist/osisoft_pi_webapi_python_client-1.2.0-py2.py3-none-any.whl --force-reinstall -I --ignore-installed

# install bdist_wheel
pip install dist/osisoft_pi_webapi_python_client-1.1.0-py2.py3-none-any.whl

# build docs
sphinx-build -b html docs/source docs/build

# run tests
nosetests --rednose

pip download \
    --only-binary=:all: \
    --platform any \
    --python-version 3 \
    --implementation py \
    --abi none \
    SomePackage


python setup.py develop



#anaconda virtual environment
source deactivate
conda env remove --name osisoftpy-dev -y
conda env create --file anaconda/dev-environment.yml
source activate osisoftpy-dev


#anaconda virtual environment
source deactivate
conda env remove --name osisoftpy-freeze -y
conda env create --file anaconda/freeze-environment.yml
source activate osisoftpy-freeze

source deactivate
conda env remove --name osisoftpy-prod -y
conda env create --file anaconda/prod-environment.yml
source activate osisoftpy-prod
activate osisoftpy-prod

pip install -r requirements.txt
pip install -r test-requirements.txt





conda env create -f environment.yml
source activate venv-conda
pip install ./dist/osisoftpy-2.0.7-py2.py3-none-any.whl

git checkout $(git rev-list -n 1 HEAD -- "structures.py")^ -- "structures.py"

git config alias.restore '!f() { git checkout $(git rev-list -n 1 HEAD -- $1)~1 -- $(git diff --name-status $(git rev-list -n 1 HEAD -- $1)~1 | grep '^D' | cut -f 2); }; f'
