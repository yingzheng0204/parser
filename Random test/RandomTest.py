# with open('param100') as f:
# 	firstLine = f.readline()
# print(firstLine)
# print(firstLine == 'System{' + '\n')
# print(firstLine[:-1])

# a = []
# a.append(1)
# a.append('1')
# print(a)

# def read(openFile):
# 	line = f.readline()
# 	return line

# with open('param100') as f:
# 	line = f.readline()
# 	print(line, end='')
# 	print(read(f), end='')
# 	line3 = f.readline()
# 	print(line3, end='')

# line = '    chi(                \n'
# line = ''
# l = line.split()
# print(len(l))

# value = "6e777777"
# if value.isdigit() == True:
# 			print('int')
# 			v = int(value)
# else:
# 	try:
# 		v = float(value)
# 		print('float')
# 	except ValueError:
# 		v = value
# 		print('string')
# print(type(v), ' ', v)

with open('random') as f:
	value = []
	att = []
	line = f.readline()
	l = line.split()
	while l[0] != ')':
		att.append(l)
		line = f.readline()
		l = line.split()
	print(att)
	rowMax = att[0][0]
	colMax = att[0][1]
	for i in range(1, len(att)):
		if att[i][0] > rowMax:
			rowMax = att[i][0]
		if att[i][1] > colMax:
			colMax = att[i][1]
	size = int(max(rowMax, colMax))+1
	for i in range(0, size):
		value.append([])
		for j in range(0, size):
			value[i].append(0)
	for i in range(0, len(att)):
		value[int(att[i][0])][int(att[i][1])] = float(att[i][2])
	print(value)


