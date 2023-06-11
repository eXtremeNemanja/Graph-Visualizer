#!/bin/bash

install_component() {
    echo "Installing $1..."
    eval "$2" &> /dev/null &

    local pid=$!
    local delay=0.1
    local progress=0
    local bar_length=30

    while kill -0 $pid &>/dev/null; do
        filled_length=$((progress * bar_length / 100))
        empty_length=$((bar_length - filled_length))

        bar="["
        for ((i = 0; i < filled_length; i++)); do
            bar+="="
        done
        for ((i = 0; i < empty_length; i++)); do
            bar+=" "
        done
        bar+="]"

        printf "\r%s %s%%" "$bar" "$progress"
        progress=$((progress + 2))
        sleep $delay
    done

    printf "\r%s %s%%\n" "[==============================]" "100"
}


install_component "Django" "pip install django"
install_component "core component" "cd core && python setup.py install"
install_component "rdf_loader component" "cd rdf_loader && python setup.py install"
install_component "xml_loader component" "cd xml_loader && python setup.py install"
install_component "json_loader component" "cd json_loader && python setup.py install"
install_component "simple_visualizer component" "cd simple_visualizer && python setup.py install"
install_component "complex_visualizer component" "cd complex_visualizer && python setup.py install"

echo "Components installed successfully."
