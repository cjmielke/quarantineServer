from sqlalchemy import Integer, String, Column, Float, Text
from sqlalchemy.dialects.mysql import INTEGER

from . import db


# Base = declarative_base()

class Ligand(db.Model):
	__tablename__ = 'zincLigands'
	zincID = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=False)

	protID = Column(Integer)

	#name = Column(String)
	smiles = Column(Text)
	InChI = Column(Text)

	weight = Column(Float)
	ph = Column(Integer)
	charge = Column(Integer)
	logP = Column(Float)

	trancheName = Column(String(6))

	'''
	subsets = db.relationship('LigandSubset')

	@property				# return as a dictionary
	def tags(self):
		tags = [subset.name for subset in self.subsets]
		return tags
	'''


class LigandSubset(db.Model):
	__tablename__ = 'zincToSubset'
	zincID = Column(INTEGER(unsigned=True), primary_key=True, index=True)
	subset = Column(Integer, primary_key=True)

class Subset(db.Model):
	__tablename__ = 'zincSubsets'
	subset = Column(Integer, primary_key=True)
	subsetName = Column(String(16), unique=True)




def getSubset(name):
	# type: (str) -> Subset
	#subset = Subset.query.get(Subset.name==name)
	subset = Subset.query.filter(Subset.subsetName == name).first()

	if subset is None:
		subset = Subset(subsetName=name)
		db.session.add(subset)
		db.session.commit()

	return subset

def getLigand(zincID):
	# type: (int) -> Ligand
	ligand = Subset.query.get(int(zincID))

	if not ligand:
		ligand = Ligand(zincID=zincID)

	return ligand

