# Server for the [Quarantine@Home](https://quarantine.infino.me/) Project. 


Central job coordination server for quarantineAtHome project. 

### Obtaining the raw data from the main server

You can obtain a full SQL dump from the production server at these two links. It is missing a few extra-large tables, and has the IP addresses trimmed from the jobs table. (See createDB.sh in this repo)

See the flatfiles at [https://quarantine.infino.me/static/](https://quarantine.infino.me/static/)

To import the sql database into your own private MySQL server :

    wget https://quarantine.infino.me/static/quarantineJobs.sql.bz2
    wget https://quarantine.infino.me/static/quarantine.sql.bz2
    bunzip *.bz2
    mysql -u root -p[yourpass] -e 'create schema quarantine;'
    mysql -u root -p[yourpass] quarantine < quarantineJobs.sql
    mysql -u root -p[yourpass] quarantine < quarantine.sql

To fetch the docked poses, we have prepared a tar archive

    cd quarantineServer # or wherever else you pulled this repository
    wget https://quarantine.infino.me/static/poses.tar.gz
    tar -xvzf poses.tar.gz


## Running the main server locally

This repo is only useful for developers. Also see the [Client codebase](https://github.com/cjmielke/quarantineAtHome)

After cloning, create a secrets.py file at app/initializers/secrets.py

    MYSQL_PASSWORD='its a secret'
    SECRET_KEY='somerandom1oi3n10i81203fi82eifn'

To run : 

    ./runserver -debug

    


### Todo
- [x] import subset'ed tranches into sql and assign them preferrentially
- [x] expose ligand metadata in frontend
- [ ] results viz improvements - template and JS configs
- [x] SMILES rendering
- [x] query caching https://flask-caching.readthedocs.io/en/latest/
- [ ] stats page with common queries and caching 
- [x] work on data exports - need to find best way to remove ip address column : https://stackoverflow.com/questions/15264597/how-to-take-mysql-dump-of-selected-columns-of-a-table

- [ ] more indexes for sql schema

- [ ] create a docker-compose file to orchestrate this along with a containerized mysql, as well as a sentry server for remote error collection



##### Running in developer mode locally with a SQLLite database

    python2.7 runserver.py


##### Running in production with MySQL

for production use, you must install the relevant mysql libraries

    sudo apt-get install libmysqlclient-dev
    pip2.7 install mysqlclient

then create a secrets.py file in app/initializers/secrets.py with the relevant
MYSQL_PASSWORD = 'password'

To run the server, pass the production flag

    python2.7 runserver.py -production



##### Client notes

This webserver also contains a "client" controller that serves up a page at '/client/' - including demo ligans and receptors.
This page, and associated coffeescript, serves as a place to develop the frontend that runs on the users client computer.
Hosting it on the main server like this permits more rapid development with coffeescript and jade/pug templates, and these are dependencies I'd rather not push onto the client stack.

Regarding the interface, this is what Im thinking.....
* Slow clients will run 1 ligand at a time, against multiple receptors
* Fast clients will download batches of several ligands at a time, and run them against multiple receptors

It's easy to use NGL to display a running queue of ligands as they come in. Could implement it as a deque.

Displaying multiple receptors is more intensive on the graphics. A client probably shouldn't display more than a handful of receptors at a time.
I can either limit the set of receptors a client works on, or I can implement a selector whereby the user chooses which receptor result to see.

* implementing a selector like this would require a /results/ subdirectory that fills with ligand structures, poses
* a list of jobs would need to be stored somewhere, storing ligand names, receptor names, energies. Could throw into sqlite, for now, JSON or txt


Endpoints :
* status.json : main polling endpoint, will have a jobID that the frontend could compare -> triggers client insert of rows to top of results table
* results.json : endpoint that returns last N jobs completed to pre-populate table






