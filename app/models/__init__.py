
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def printSchema(model):
	# Neat trick to print the create table syntax that would be sent to the server
	from sqlalchemy.schema import CreateTable
	#model = Results
	print(CreateTable(model.__table__))