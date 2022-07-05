#!/usr/bin/env bash


create_output(){
  output_file="output-$(cut -d "-" -f2- <<< $1)"
  var='output!0'
  pwd
  gcc $2 -lm
  output=$(./a.out < $1)
  echo $output
  echo "(declare-const ${var} (_ BitVec 32))  (assert (= ${var} (_ bv${output} 32)))" > "test_${output_file}.smt2"
  retval="test_${output_file}.smt2:klee-${file} "
}

save=$(pwd)
cd /home/Trident/Trident/runtime || return
KLEE_INCLUDE_PATH=/klee/include make

cd $save || return

PROGRAM=$(realpath $1)
echo $PROGRAM
goto=$(dirname $PROGRAM)
cd $goto

TRIDENT_CC="/home/Trident/Trident/main/trident-cc"

if [ -f "$PROGRAM" ]; then
make clean
fi

CC="$TRIDENT_CC" make -e
NEW_PROGRAM="${PROGRAM::-2}"
extract-bc "${NEW_PROGRAM}"
files=$(ls|grep "^input-.*")
cnt=1
array=()
for file in $files
  do
    if [ $2 == "klee-merge" ]
    then
    timeout -k 600s 600s klee --posix-runtime --libc=uclibc -use-merge --write-smt2s -write-kqueries \
    --output-dir=klee-"${file}" --max-time 300 -max-solver-time 100 --max-forks 500 "${NEW_PROGRAM}.bc"  < "${file}"
    else
    timeout -k 600s 600s klee --posix-runtime --libc=uclibc  --write-smt2s -write-kqueries \
    --output-dir=klee-"${file}" --max-time 300 -max-solver-time 100 --max-forks 500 "${NEW_PROGRAM}.bc"  < "${file}"
    fi
    create_output "${file}" "${PROGRAM}.expected.c"
    array+=$retval
  done


if [ $3 == "--priority" ]
then
timeout -k 600s 600s python3.6 /home/Trident/Trident/main/synthesis.py --priority --tests ${array[*]} \
   --components /home/Trident/Trident/components/*.smt2
else
timeout -k 600s 600s python3.6 /home/Trident/Trident/main/synthesis.py --tests ${array[*]} \
   --components /home/Trident/Trident/components/*.smt2
fi

make clean 1>/dev/null

