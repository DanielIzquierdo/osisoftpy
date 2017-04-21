# install dev dependencies
# add colors to nosetests
pip install rednose

# clean ./build
python setup.py clean --all
python setup.py sdist
python setup.py bdist_wheel
pip install dist/osisoft_pi_webapi_python_client-1.2.0-py2.py3-none-any.whl --force-reinstall -I --ignore-installed

# install bdist_wheel
pip install dist/osisoft_pi_webapi_python_client-1.1.0-py2.py3-none-any.whl

# run tests
nosetests --rednose
