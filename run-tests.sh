

__quiet() {
  $@ > /dev/null
}


__silence() {
  $@ 2>&1 > /dev/null
}

__setup_venv() {
  rm -rf venv$1
  __python=python$1
  which python$1 > /dev/null
  if [ "$?" != "0" ]
  then
    if [ "$1" = "2" ]
    then
      __python=python
    fi
  fi
  (>&2 echo "  Python$1 ($(which $__python)) -> venv$1")
  virtualenv -p $__python venv$1

  . venv$1/bin/activate
  pip install .
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

__prefix="__quiet"
if [ "$1" = "-v" ]
then
  __prefix=""
elif [ "$1" = "-s" ]
then
  __prefix="__silence"
fi

echo "----Creating Python virtual environments----"
$__prefix __setup_venv 2 &
$__prefix __setup_venv 3 &
wait
echo "----done----"
echo
__do_tests 2
__do_tests 3
