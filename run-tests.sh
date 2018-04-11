__setup_venv() {
  echo "----Creating Python$1 virtual envrionment in venv$1----"
  rm -rf venv$1
  virtualenv -p python$1 venv$1
  echo "----Installing vimcryption into venv$1----"
  venv$1/bin/pip install nose2
  venv$1/bin/python testsetup.py install
  echo "----done----"
}

__do_tests() {
  echo "--Running Python$1 Tests--"
  venv$1/bin/nose2 -s plugin/
  echo "---------Complete---------"
  echo
}

__setup_venv 2
__setup_venv 3
echo
__do_tests 2
__do_tests 3
