import re

names = []
with open("boynames.html") as f:
    names = re.findall(r"<li>(\w+)", f.read())
