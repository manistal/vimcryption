

__setup_venv() {
  echo "----Creating Python$1 virtual envrionment in venv$1----"
  rm -rf venv$1
  if [ $1 == '2' ]; then 
    virtualenv -p python venv$1 # Mac's python install doesn't have "python2"
  else
    virtualenv -p python$1 venv$1
  fi

  . venv$1/bin/activate
  echo "----Installing vimcryption into venv$1----"
  pip install .
  echo "----done----"
}

__do_tests() {
  echo "--Running Python$1 Tests--"
  . venv$1/bin/activate
  nose2 -s test/
  echo "---------Complete---------"
  echo
}

export ORIG_PYPATH=$PYTHONPATH
export ORIG_PYBYTECODE=$PYTHONDONTWRITEBYTECODE

export PYTHONPATH=$PYTHONPATH:$PWD/plugin
export PYTHONDONTWRITEBYTECODE=1

__setup_venv 2
__setup_venv 3
echo
__do_tests 2
__do_tests 3

export PYTHONPATH=ORIG_PYPATH
export PYTHONDONTWRITEBYTECODE=ORIG_PYBYTECODE

