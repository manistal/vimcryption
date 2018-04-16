

__setup_venv() {
  echo "----Creating Python$1 virtual envrionment in venv$1----"
  rm -rf venv$1
  __python=python$1
  which python$1
  if [ "$?" != "0" ]
  then
    if [ "$1" = "2" ]
    then
      __python=python
    fi
  fi
  virtualenv -p $__python venv$1

  . venv$1/bin/activate
  echo "----Installing vimcryption into venv$1----"
  which $__python
  pip install .
  which nose2
  ls venv$1/bin/
  echo "----done----"
}

__do_tests() {
  echo "--Running Python$1 Tests--"
  . venv$1/bin/activate
  __python=python$1
  if [ "$1" = "2" ]
  then
    __python=python
  fi
  which $__python
  nose2 -s test/
  echo "---------Complete---------"
  echo
}

#export PYTHONPATH=$PYTHONPATH:$PWD/plugin
export PYTHONDONTWRITEBYTECODE=1

__setup_venv 2
__setup_venv 3
echo
__do_tests 2
__do_tests 3
