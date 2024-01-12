#!/usr/bin/env bash

main() {
    echo '!'

    if [[ $# -gt 0 ]]
    then
        args=( "$@" )
        args_no_last=( ${@:1:$#-1} )
    
        for arg in "${args[@]}"
        do
            echo "$arg"
        done
    fi

    # add code here
    git add .
    git commit -m "$1"
    ./archive.sh
    ./ansible-setup.sh
    
}

main "$@"

