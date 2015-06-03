f = open("TransactionHistory.csv")
headers = True

data = []

if(headers):
	f.readline()
for line in f.readlines():
	try:
		data.append(line.split(",")[3])
	except:
		pass

for item in data:
	a = item
	b = a.split(" ")
	c = " ".join(a.split())
	c.split(" ")
	d = c.split(" ")
	e = ""
	for word in d:
		if(len(word) == 0):
			continue
		elif(any(c.isdigit() for c in word)):
			#print word, (sum(c.isdigit() for c in word) / float(len(word)))
			if((sum(c.isdigit() for c in word) / float(len(word))) <= 0.2): # if less than 20% are numbers
				e += word + " "
				continue
			elif(len(e)>0):
				break
			continue
		e += word + " "
	if len(word) != 0:
		print e