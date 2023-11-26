#!/bin/bash
#

set -eu -o pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <day>"
    exit 1
fi

source ~/.aoc2023

a=$( echo "${1}" | bc )
b=$( printf %02d "${a}" )

mkdir -p "${b}"

curl -s -b "session=${sessionkey}" "https://adventofcode.com/2023/day/${a}/input" > "${b}"/input

cat "${b}"/input
wc "${b}"/input
