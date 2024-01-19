main() {
    echo 'Bash: hello world!'
    if [[ $# -eq 0 ]]
    then
        return
    fi
    args=( "$@" )
    args_no_last=( ${@:1:$#-1} )
    
    for arg in "${args[@]}"
    do
        echo "$arg"
    done

    # Add your code here
    python3 -m flask main run
}

main "$@"
