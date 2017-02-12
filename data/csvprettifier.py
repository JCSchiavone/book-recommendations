import pickle
with open('clusteredshelves.csv', 'rb') as f:
	lines = f.read().lower().split('\r')
	rows = [line.split(",") for line in lines]
	d = {}
	for row in rows:
		d[row[1]]=row[0]

with open('shelf_mappings.p', 'wb') as f:
	pickle.dump(d,f)
