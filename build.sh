# clean ./build
python setup.py clean --all

# build  source distibution
python setup.py sdist

# build python wheel
python setup.py bdist_wheel
