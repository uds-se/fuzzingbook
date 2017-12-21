#!/bin/sh
# TextMate drop-in replacement for pdflatex

# Thank you, stackoverflow
opts="${@:1:$# -1}"
last="${@: -1}"

# The main file
main=gstbook

# Weaving options
pweave="pweave -f texminted"

# Ensure we have weave in our path
PATH=/opt/local/Library/Frameworks/Python.framework/Versions/3.6/bin/:$PATH

source="$last"
case $source in
??-*.texw)
    # Include and weave only one chapter
    all=false
    base=$(basename "$source" .texw)
    echo "\\includeonly{$base}" > include.tex
    $pweave "$source"
    ;;
*.texw)
    # Include all; weave all files
    all=true
    base=$(basename "$source" .texw)
    echo "" > include.tex
    for chapter in ??-*.texw; do
        $pweave $chapter
    done
    $pweave "$source"
    ;;
*.tex)
    # Just regular PDFLaTeX; no weaving
    all=true
    main=$(basename "$source" .tex)
    ;;
esac

# Now run PDFLaTeX on the main file (with the appropriate \includeonly)
pdflatex $opts -shell-escape "$main".tex
status=$?

# Move target to appropriate PDF
if $all; then
    :
else
    mv "$main".pdf "$base".pdf
    echo "Output file is $base.pdf"
fi
exit $status