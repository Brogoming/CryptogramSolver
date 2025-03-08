import re

txt = "4534a53"
x = re.search("^[a-z']+$",txt)
print(x)