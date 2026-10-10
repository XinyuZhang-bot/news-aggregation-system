#!/bin/sh
if [ "$1" = "build" ];then
    mkdir /home/changsheng/project/project87553/project
    cp -a /home/changsheng/project/project87553/server/. /home/changsheng/project/project87553/project/
    cd /home/changsheng/project/project87553/project
    rm -rf /home/changsheng/project/project87553/server
    echo "执行成功"
fi
