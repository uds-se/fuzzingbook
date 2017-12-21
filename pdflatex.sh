#!/bin/sh
# TextMate drop-in replacement for pdflatex

# Usage: ./pdflatex.sh OPTIONS SOURCE
# where SOURCE is a ,texw input file

# Thank you, stackoverflow
opts="${@:1:$# -1}"
last="${@: -1}"

# The main file
main=gstbook

# Weaving options
pweave="pweave -f texminted"

# Weave
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

# Fix the resulting .synctex.gz table (if any)
# This only fixes file names, not line numbers
if [ -f "$main".synctex.gz ]; then
    gunzip "$main".synctex.gz
    sed 's/\.tex$/\.texw/' "$main".synctex | gzip > "$main".synctex.gz
    rm "$main".synctex
    echo "Fixed SyncTeX file to point back to .texw file."
fi

# Move target to appropriate PDF
if $all; then
    :
else
    mv "$main".pdf "$base".pdf
    if [ -f "$main".synctex.gz ]; then
        mv "$main".synctex.gz "$base".synctex.gz
        echo "SyncTeX moved to $base.synctex.gz."
    fi
    echo "Output written to $base.pdf."
fi
exit $status
