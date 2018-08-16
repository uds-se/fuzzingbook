#!/bin/sh
# Some fixes to exported .py files

sed 's/^import gstbook$/# & # only in notebook/' | \
sed "s/^get_ipython().run_cell_magic([^,]*, [^,]*, '\([^']*\)').*$/\1/" | \
sed 's/^get_ipython().*/# & # only in notebook/'
