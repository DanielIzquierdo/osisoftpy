# install dev dependencies
# add colors to nosetests
pip install rednose

# clean ./build
python setup.py clean --all

# build  source distibution
python setup.py sdist

# build python wheel
python setup.py bdist_wheel

# install bdist_wheel
pip install dist/osisoft_pi_webapi_python_client-1.1.0-py2.py3-none-any.whl

# run tests
nosetests --rednose
