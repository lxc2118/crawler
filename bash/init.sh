#!/bin/bash

vimrc_path=~/.vimrc.bak
id_rsa_path=~/.ssh/id_rsa.pub

mk_file() {
    if [ ! -e $1 ]
    then
        if [ -d ${1%/*} ]
        then
            echo "mkfile:" $1
            touch $1
        else
            echo "mkdir and file" ${1%/*}
            mkdir -p ${1%/*}
            touch $1
        fi
    fi
}

init_vimrc() {
    echo "init vimrc"
    "set nu" >> $1
    "set ts=4" >> $1
    "set shiftwidth=4" >> $1
    "set smartindent" >> $1
    "set expandtab" >> $1
    "set hlsearch" >> $1
    "%retab" >> $1
}

init_git() {
    mk_file $id_rsa_path
}


