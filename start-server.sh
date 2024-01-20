main() {
    
    if [[ $# -eq 0 ]]
    then
        # Add your code here
        echo 'activating virtual env..'
        . ../venv/bin/activate
        echo 'installing dependencies..'
        python3 -m pip install -r requirements.txt
        echo 'starting server'
        python3 -m flask --app trending.py --debug run
    fi
    args=( "$@" )
    args_no_last=( ${@:1:$#-1} )
    
    for arg in "${args[@]}"
    do
        echo "$arg"
    done


}

main "$@"
