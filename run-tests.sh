

__setup_venv() {
  echo "----Creating Python$1 virtual envrionment in venv$1----"
  rm -rf venv$1
  if [ $1 == '2' ]; then 
    virtualenv -p python venv$1 # Mac's python install doesn't have "python2"
  else
    virtualenv -p python$1 venv$1
  fi

  echo "----Installing vimcryption into venv$1----"
  venv$1/bin/pip install nose2
  venv$1/bin/python testsetup.py install

  echo "----done----"
}

__do_tests() {
  echo "--Running Python$1 Tests--"
  venv$1/bin/nose2 -s test/
  echo "---------Complete---------"
  echo
}

export ORIG_PYPATH=$PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PWD/plugin

__setup_venv 2
__setup_venv 3
echo
__do_tests 2
__do_tests 3

export PYTHONPATH=ORIG_PYPATH

