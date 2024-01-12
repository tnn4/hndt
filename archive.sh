#!/usr/bin/env bash

main() {
    echo 'Archiving...'

    if [[ $# -gt 0 ]]
    then
        args=( "$@" )
        args_no_last=( ${@:1:$#-1} )
    
        for arg in "${args[@]}"
        do
            echo "$arg"
        done
    fi
    VERSION=$(<VERSION)
    # add code here
    echo v${VERSION}
    git archive -o archive/hn-data-tools-v"${VERSION}".zip HEAD
}

main "$@"

