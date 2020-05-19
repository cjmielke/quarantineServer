#!/bin/bash

# pass root password of sql database to this script

mysql -u root -p$1 -e "USE quarantine; SHOW TABLES;"

mysqldump --ignore-table quarantine.jobs --ignore-table quarantine.zincToTrancheFile -u root -p$1 quarantine > quarantine.sql


mysql -u root -p$1 -e "create table quarantinepublic.jobs as select * from quarantine.jobs;"
mysql -u root -p$1 -e "update quarantinepublic.jobs set ip=NULL;"
mysqldump -u root -p$1 quarantinepublic > quarantineJobs.sql
mysql -u root -p$1 -e "drop table quarantinepublic.jobs;"


#bzip2 *.sql
#rm quarantine.sql
#rm quarantineJobs.sql


#mysql -u root -p$1 -e ""
#mysql -u root -p$1 -e ""



