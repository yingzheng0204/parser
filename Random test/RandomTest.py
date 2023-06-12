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

# with open('random') as f:
# 	value = []
# 	att = []
# 	line = f.readline()
# 	l = line.split()
# 	while l[0] != ')':
# 		att.append(l)
# 		line = f.readline()
# 		l = line.split()
# 	print(att)
# 	rowMax = att[0][0]
# 	colMax = att[0][1]
# 	for i in range(1, len(att)):
# 		if att[i][0] > rowMax:
# 			rowMax = att[i][0]
# 		if att[i][1] > colMax:
# 			colMax = att[i][1]
# 	size = int(max(rowMax, colMax))+1
# 	for i in range(0, size):
# 		value.append([])
# 		for j in range(0, size):
# 			value[i].append(0)
# 	for i in range(0, len(att)):
# 		value[int(att[i][0])][int(att[i][1])] = float(att[i][2])
# 	print(value)

# with open('random') as f:
# 	value = []
# 	line = f.readline()
# 	l = line.split()
# 	while l[0] != ']':
# 		if len(l) == 1:
# 			value.append(l[0])
# 		if len(l) == 2:
# 			value.append([l[0], l[1]])
# 		line = f.readline()
# 		l = line.split()
# 	print(value)

# class Dummy(object):
#     def __getattr__(self, attr):
#     	print(attr)
#     	return attr.upper()
# d = Dummy()
# print(d.does_not_exist) # 'DOES_NOT_EXIST'
# d.what_about_this_one  # 'WHAT_ABOUT_THIS_ONE'

# with open('writeTest', 'w') as f:
# 	depth = '  '
# 	label = 'chi'
# 	value = [[0, 10], [10, 0]]
	
# 	s = ''
# 	s = s + depth + label + '(\n'
# 	for i in range(0, len(value)):
# 		for j in range(0, i+1):
# 			s = s + depth + f'{i:>24}{j:>5}   ' + f'{value[i][j]:.12e}\n'
# 	s = s + depth + ')\n'
	
# 	f.write(s)

with open('writeTest', 'w') as f:
	depth = '  '
	# label = 'mesh'
	# label = 'type'
	# label = 'vMonomer'
	label = 'isShell'
	# value = [36, 36, 36]
	# value = 100
	# value = 'linear'
	# value = 1.0
	value = 0

	s = ''
	if label == 'mesh':
		s += depth + f'{label:40}'
		if type(value) is list:
			s += f'{value[0]:>6}'
			for i in range(1, len(value)):
				s += f'{value[i]:>7}'
			s += '\n'
		else:
			s += f'{value:6}\n'
	else:
		s += depth + f'{label:20}'
		if type(value) is float:
			v = f'{value:.12e}'
			s += f'{v:>20}\n'
		else:
			s += f'{value:>20}\n'
	
	f.write(s)