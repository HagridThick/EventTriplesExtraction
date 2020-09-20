line = 'asdf fjdk; afed, fjek,asdf, foo'
import re
str1 = re.split(r'[,]\s*', line)
print(str1)