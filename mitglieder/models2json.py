#/bin/python
import re

f = open('backend/mitgliederverwaltung/mitglieder/models.py')
ll = f.readlines()
f.close()


regex = r"class (\w+)\(models\.Model\):"

r = re.compile(regex)
newlist = list(filter(r.match, ll))
print(newlist)
