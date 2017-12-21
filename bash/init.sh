#!/bin/bash

vimrc_path=~/.vimrc.bak
id_rsa_path=~/.ssh/id_rsa.pub
apt_sources_path=/etc/apt/sources.list

pip2_lib=(
    pep8
    pygments
    sh
    argparse
    lxml
    xmltodict
    requests
    pdb mako
    matplotlib
    numpy
    pandas
)

pip3_lib=()


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

init_apt_source() {
    echo "init_apt_source"
    \rm -rf /var/lib/apt/lists/
    "deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted" > $1
    "deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted" >> $1
    "deb http://mirrors.aliyun.com/ubuntu/ xenial universe" >> $1
    "deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe" >> $1
    "deb http://mirrors.aliyun.com/ubuntu/ xenial multiverse" >> $1
    "deb http://mirrors.aliyun.com/ubuntu/ xenial-updates multiverse" >> $1
    "deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse" >> $1
    "deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted" >> $1
    "deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe" >> $1
    "deb http://mirrors.aliyun.com/ubuntu/ xenial-security multiverse" >> $1
    echo "apt-get update"
    apt-get update
}

pip2_install() {
    for lib in ${pip2_lib[@]};
    do
        pip2 install $lib
        pip2 install --upgrade $lib
    done
}

pip3_install() {
    for lib in ${pip3_lib[@]};
    do
        pip3 install $lib
        pip3 install --upgrade $lib
    done
}

init_git() {
    mk_file $id_rsa_path
    git config --global user.name $git_name
    git config --global user.email %git_email
    git config color.ui true
}

ss_qt5_install() {
    add-apt-repository ppa:hzwhuang/ss-qt5
    apt-get update
    apt-get install shadowsocks-qt5
}

apt_get_install() {
    apt-get install openssh-server
    apt-get install tig
    apt-get install sqlitebrowser
    apt install python-pip
    apt install python3-pip
    apt install xpad
}