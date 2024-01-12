#!/usr/bin/env bash

main() {
    echo 'Setting up HN API data cacher remotely.'

    if [[ $# -gt 0 ]]
    then
        args=( "$@" )
        args_no_last=( ${@:1:$#-1} )
    
        for arg in "${args[@]}"
        do
            echo "$arg"
        done
    fi

    if  ! command -v ansible-playbook &> /dev/null
    then
        echo 'This script requires ansible'
        echo 'Try: sudo apt install ansible'
        return
    fi
    # These are the commands you want to run on the host
    SETUP_PLAYBOOK="ansible-setup.yml"
    RUN_PLAYBOOK="ansible-run.yml"
    # Inventory containes list of hosts
    INV="ansible-inventory.yml"

    if [[ $# -eq 0 ]]
    then
        OPTION='setup'
    else
        OPTION=$1
    fi
    #fi
    # add code here
    if [[ $OPTION == 'setup' ]]
    then
        ansible-playbook --ask-pass --ask-become-pass --inventory ${INV} ${SETUP_PLAYBOOK}
    elif [[ $OPTION == "run" ]]
    then
        ansible-playbook --ask-pass --inventory ${INV} ${RUN_PLAYBOOK}
    fi
}

main "$@"

