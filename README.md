# quarantineServer
Central job coordination server for quarantineAtHome project. This is implemented as a simple https API with a sql backend for now. Jobs are handed out sequentially for the time being, but later versions will implement a proper system for prioritizing more important computational needs.

This repo is only useful for developers. After cloning, create a secrets.py file at app/initializers/secrets.py

    MYSQL_PASSWORD='its a secret'
    SECRET_KEY='somerandom1oi3n10i81203fi82eifn'

To run : 

    ./runserver -debug
  

### Todo
- [ ] work on data exports - need to find best way to remove ip address column : https://stackoverflow.com/questions/15264597/how-to-take-mysql-dump-of-selected-columns-of-a-table

- [ ] define indexes for sql schema

- [ ] create a docker-compose file to orchestrate this along with a containerized mysql, as well as a sentry server for remote error collection



##### Running in developer mode locally

    python2.7 runserver.py


##### Running in production



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






