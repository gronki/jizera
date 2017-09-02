#!/bin/bash

buildone() {
echo $1
coffee -pb ${1} > ../../jizera/static/js/${1%.coffee}.js
}

for f in *.coffee; do
	buildone ${f}
done
