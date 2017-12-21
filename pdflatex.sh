#!/bin/sh
# TextMate drop-in replacement for pdflatex

# Thank you, stackoverflow
opts="${@:1:$# -1}"
last="${@: -1}"

# The main file
main=gstbook

source="$last"
case $source in
*.tex)
    # Include only chapter
    all=false
    base=$(basename "$source" .tex)
    echo "\\includeonly{$base}" > include.tex
    ;;
*.texw)
    # Include all
    all=true
    base=$(basename "$source" .texw)
    echo "" > include.tex
    ;;
esac

# Weave (with the appropriate include)
PATH=/opt/local/Library/Frameworks/Python.framework/Versions/3.6/bin/:$PATH
pweave -f texminted "$main".texw

# Now run PDFLaTeX on the main file
pdflatex $opts "$main".tex
status=$?

# Move target to appropriate PDF
if $all; then
    :
else
    mv "$main".pdf "$base".pdf
    echo "Output file is $base.pdf"
fi
exit $status