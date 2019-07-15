#!/bin/sh

printenv | sed 's/^\(.*\)$/export \1/g' > ${HOME}/.env.sh
chmod +x ${HOME}/.env.sh

cron -f
