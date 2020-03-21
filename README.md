# quarantineServer
Central job coordination server for quarantineAtHome project. This is implemented as a simple https API with a sql backend for now. Jobs are handed out sequentially for the time being, but later versions will implement a proper system for prioritizing more important computational needs.

This repo is only useful for developers. After cloning, create a secrets.py file at app/initializers/secrets.py

  MYSQL_PASSWORD='its a secret'
  SECRET_KEY='somerandom1oi3n10i81203fi82eifn'

To run : 

  ./runserver -debug
  

