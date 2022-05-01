#!/bin/sh

top="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"

echo "top: ${top}"

mkdir -p build
cd build

GRAPHVIZ_DIR=graphviz-3.0.0
GRAPHVIZ_TGZ=${GRAPHVIZ_DIR}.tar.gz

if test ! -f ${GRAPHVIZ_TGZ}; then
    wget https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/3.0.0/${GRAPHVIZ_TGZ}
    if test $? -ne 0; then exit 1; fi
fi

if test -d ${GRAPHVIZ_DIR}; then
  rm -rf ${GRAPHVIZ_DIR}
fi

tar xvzf ${GRAPHVIZ_TGZ}
if test $? -ne 0; then exit 1; fi

cd ${GRAPHVIZ_DIR}
./configure --prefix=`pwd`/inst \
	--disable-shared --enable-static
if test $? -ne 0; then exit 1; fi

make
if test $? -ne 0; then exit 1; fi

make install
if test $? -ne 0; then exit 1; fi

ls -l inst/bin/dot_static
strip inst/bin/dot_static
ls -l inst/bin/dot_static

