#!/bin/sh

if [ $# -ne 2 ]; then
    echo Usage: "$0 <PATH> <BASE>" >&2
    exit 1
fi

exec perl -M5.01 -MFile::Spec -e "say abs2rel File::Spec @ARGV" "$1" "$2"
