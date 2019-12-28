fr = open('test.txt', 'r')
result = fr.read()
fr.close()

result = result.replace('java', 'python')

fw = open('test.txt', 'w')
fw.write(result)
fw.close()
