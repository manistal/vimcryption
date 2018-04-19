

__quiet() {
  $@ > /dev/null
}


__silence() {
  $@ 2>&1 > /dev/null
}

__get_python_interpreter_path() {
  __python=python$1
  which $__python > /dev/null
  if [ "$?" != "0" ]
  then
    if [ "$1" = "2" ]
    then
      __python=python
    fi
  fi
  __python=$(which $__python)
  echo $__python
}

__setup_venv() {
  rm -rf venv$1
  __python=$(__get_python_interpreter_path $1)
  (>&2 echo "    python$1 ($__python) -> venv$1")
  $(dirname $__python)/virtualenv -v -p $__python venv$1

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

__versions=(
  2
  3
)

echo "Creating Python virtual environments"
declare -A __pids
declare -A __rcs
for __version in "${__versions[@]}"
do
  $__prefix __setup_venv $__version &
  __pids[$__version]=$!
done

for __version in "${!__pids[@]}"
do
  wait ${__pids[$__version]}
  __rcs[$__version]=$?
done

echo "done."
echo
for __version in "${__versions[@]}"
do
  __do_tests $__version
done
