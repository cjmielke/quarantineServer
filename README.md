# quarantineServer
Central job coordination server for quarantineAtHome project. This is implemented as a simple https API with a sql backend for now. Jobs are handed out sequentially for the time being, but later versions will implement a proper system for prioritizing more important computational needs.

This repo is only useful for developers. After cloning, create a secrets.py file at app/initializers/secrets.py

    MYSQL_PASSWORD='its a secret'
    SECRET_KEY='somerandom1oi3n10i81203fi82eifn'

To run : 

    ./runserver -debug
  

### Todo

* make a simple results page for public consumption
* define indexes for sql schema

* create a docker-compose file to orchestrate this along with a containerized mysql, as well as a sentry server for remote error collection
