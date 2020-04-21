

# to install dependencies :
# sudo apt-get install python-rdkit librdkit1 rdkit-data



import argparse
import os

from flask import Flask
from flask import render_template
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from HTMLParser import HTMLParser

from sqlalchemy import text

from app.models import db


SVG_PATH = os.path.join(os.getcwd(), 'app', 'static', 'ligandsvg')


parser = argparse.ArgumentParser()
parser.add_argument('-production', action='store_true')
parser.add_argument('-scan', action='store_true')
parser.add_argument('-load', action='store_true')
parser.add_argument('-special', action='store_true')
args = parser.parse_args()

debug = True
if args.production: debug = False



def smitosvg(smi, molSize=(400, 200), outFile=None):
	mol = Chem.MolFromSmiles(smi)
	mc = Chem.Mol(mol.ToBinary())
	if not mc.GetNumConformers():
		rdDepictor.Compute2DCoords(mc)
	drawer = rdMolDraw2D.MolDraw2DSVG(molSize[0], molSize[1])
	opts = drawer.drawOptions()
	drawer.DrawMolecule(mc)
	drawer.FinishDrawing()
	svg = drawer.GetDrawingText()
	svg = svg.replace('svg:', '')

	if outFile:
		with open(outFile, 'w') as fh:
			fh.write(svg)

	return svg

smiles = 'Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(C[C@H](O)[C@H](O)[C@H](O)CO)c2cc1C'
svg = smitosvg(smiles, (150,100))




def drawRows(rows):
	for row in rows:
		if row.smiles:
			svgFile = os.path.join(SVG_PATH, '%s.svg' % str(row.zincID))
			if not os.path.exists(svgFile):
				print 'no svg file found - drawing'
				smitosvg(row.smiles, (200, 100), outFile=svgFile)
				print svgFile


def drawNeededLigands():

	from app.core import create_app
	app = create_app(debug=debug)
	with app.app_context():

		print 'looking for top ligands to draw'

		query = text('''
		select *, group_concat(subsetName) as subsets
		FROM jobs
		join zincLigands using(zincID)
		join zincToSubset using (zincID)
		join zincSubsets using (subset)
		LEFT JOIN users USING(user)
		LEFT JOIN tranches using(trancheID)
		WHERE subsetName IN ('fda')
		group by jobID
		order by bestDG 
		LIMIT 1000
		;''')
		rows = db.engine.execute(query)
		# rows = [r for r in rows]

		drawRows(rows)


if __name__=='__main__':
	drawNeededLigands()



