#!/bin/bash

HOSTS="hosts"
USER="root"
PASSWORD="password"

for HOST in $(cat ${HOSTS})
do
  expect ssh-copy-id.expect ${USER}@${HOST} ${PASSWORD}
done
