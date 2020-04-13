from sqlalchemy import text

from app.core import app
from app.models import db
from app.models.jobs import encryptIP, decryptIP
from app.models.test import testModels
from app.util import strip_tags, safer

# make sure ip address encryption/decryption is working

debug=True

with app.app_context():

	sql = text('''select ip from jobs;''')

	rows=db.engine.execute(sql)

	for row in rows:
		enc = encryptIP(row.ip)
		dec = decryptIP(enc)
		assert row.ip==dec

		print row.ip, enc, dec



