#!/bin/bash
/etc/init.d/rabbitmq-server start
su -c "bash /startup-user.sh" ${FB_USER}
