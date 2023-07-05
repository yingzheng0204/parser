
'''
File Contents:
	class Value:
		A Value object stores the value of a single string that represents all or part
		part of the value of a parameter. It could implement code to figure out the 
		type of values among string, integer and floating point.
	class Composite:
		A Composite object can be identified by opening and closing curly brackets
		('{' and '}'). It can parse a parameter file block and store its contents
		in a form that allows particular types of items within it to be accessed 
		and modified.
	class Parameter:
		A Parameter object contains a parameter label and its value for the individual 
		parameter within a single line.
	class Array:
		An Array object is a type of parameter that has values stored as elements of
		a one-dimensional array which is given in a multi-line format in which the
		first row contains a label that contains the name of the array followed 
		immediately by an opening square bracket ('['') and the last line contains a 
		matching closing square bracket (']') itself. Elements of the
		one-dimentional array are in between these delimiters with one element per
		line and appear in order of increasing array index started from 0. 
	class Matrix:
		A Matrix object is a type of parameter that has values stored as elements of
		a matrix or two-dimensional array in element format that the value of each
		nonzero element of the matrix appears on separate line. The element format 
		for a matrix starts with a line that contains a name label followed 
		immediately by an opening parenthesis and ends with a line contains a matching 
		closing paranthesis itself. In between, each line contains a row index, a 
		column index and value of a single element of the array. 
'''

# Value class ----------------------------------------------------------------------	

class Value:
	'''
	Purpose: 
		The class represents the object type that store the single value for parameters 
		of the parameter file by distinguishing the exact type of it
	Instance variables:
		val: variable to store a single value of the parameters
		type: the type of the value stored, either integer, floating point or string
	Methods:
		__init__(self, val):
			the constructor of the Value object for initiation, with one argument:
				val, the string represents the value needed to be stored for the Value object
			that initiate the value stored with its correct type
		getType(self): return the type of stored value
		getValue(self): return the value of stored value
	Note:
		Debugging by the commented line to check if the constructor has the expected 
		function of distinguishing the exact type of the value

	'''
	def __init__(self, val):
		if val.isdigit() == True:
			# print('int')
			self.val = int(val)
		else:
			try:
				self.val = float(val)
				# print('float')
			except ValueError:
				self.val = val
				# print('string')
		# print(self.value)
		self.type = type(self.val)

	def getType(self):
		return self.type

	def getValue(self):
		return self.val

# End class Value ---------------------------------------------------------

# Composite class ---------------------------------------------------------

class Composite:
	'''
	Purpose:
		The class represents the Copmosite element of the parameter file
	Instance variables:
		label: the label of the Composite element 
		children: 
			the children items of the Composite in the parameter file, defult 
			to be an empty dictionary
	Methods:
		__init__(self, label=None, file=None):
			the constructor of the Composite object for initiation, with four 
			arguments: 
				label, the label of the Composite, defult to be None; 
				file, the variable represents the filename or a open file;
			that initiate the label and the parent of the Composite object, and 
			pass in the open file for reading
		read(self, openFile):
			method to read the open parameter file, openFile as the argement, line 
			by line and update the read items into the children variable; reading 
			stop when '}' is read
		addChild(self, child):
			method to add the single item, argument child, into the children variable
		getChildren(self):
			return the children variable
		__repr__(self):
			return the string of children variable, in the dictionary format string
		__getattr__(self, attr):
			return the value stored in children with the specific key, argument attr
		writeOut(self, filename):
			method to write out the Composite element to a specific txt file with name
			of the argument filename
		writeOutString(self, depth):
			return the string for writting out with argument depth, the string of 
			spaces that represents the level of the Composite element
		returnData(self):
			return the Composite object itself
		__setattr__(self, label, val):
			set the new value, argument val, to the specific child of the Composite in
			the children dictionary, with the name of argument label
	'''
	def __init__(self, file=None, label=None):
		self.label = label
		self.children = {}

		if file != None:
			if type(file) == str:
				with open(file) as f:
					firstLine = f.readline()
					fl = firstLine.split()
					if fl[0][-1] != '{':
						raise Exception('This is not a valid parameter file.')
					else:
						self.label = fl[0][:-1]
						self.read(f)
			else:
				self.read(file)

	def read(self, openFile):
		line = openFile.readline()
		l = line.split()
		while line != '':
			if l[0][-1] == '{':
				if len(l) == 1:
					p = Composite(openFile, l[0][:-1])
				else:
					raise Exception('Not valid syntax for Composite element.')
			elif l[0][-1] == '[':
				if len(l) == 1:
					p = Array(l[0][:-1], openFile, None)
				else:
					val = []
					if l[-1] == ']':
						for i in range(1, len(l)-1):
							val.append(Value(l[i]))
						p = Array(l[0][:-1], None, val)
					else:
						for i in range(1,len(l)):
							val.append(Value(l[i]))
						p = Array(l[0][:-1], openFile, val)	
			elif l[0][-1] == '(':
				if len(l) == 1:
					p = Matrix(l[0][:-1], openFile)
				else:
					raise Exception('Not valid syntax for Matrix element.')
			elif l[0] == '}':
				break
			else:
				if len(l) == 2:
					p = Parameter(l[0], l[1])
				else:
					val = []
					for i in range(1, len(l)):
						val.append(Value(l[i]))
					p = Parameter(l[0], val)
			self.addChild(p)	
			line = openFile.readline()
			l = line.split()

	def addChild(self, child):
		label = child.label
		if label in self.children:
			self.children[label] = [self.children[label]]
			self.children[label].append(child)
		else:
			self.children[label] = child

	def getChildren(self):
		return self.children

	def __repr__(self):
		return self.writeOutString()

	def __getattr__(self, attr):
		if attr =='children':
			return {}
		if attr in self.children:
			if type(self.children[attr]) is list:
				return self.children[attr]
			else:
				return self.children[attr].returnData()
		else:
			return self.attr

	def writeOut(self, filename):
		with open(filename, 'w') as f:
			f.write(self.writeOutString())

	def writeOutString(self, depth=''):
		s = depth + self.label + '{' + '\n'
		for item in self.children.values():
			if type(item) is list:
				for i in range(len(item)):
					s += item[i].writeOutString(depth+'  ')
			else:
				s += item.writeOutString(depth+'  ')
		s += depth + '}\n'
		return s

	def returnData(self):
		return self
		
	def __setattr__(self, label, val):
		if label in self.children:
			self.children[label].setValue(val)
		else:
			self.__dict__[label] = val

# End class Composite ---------------------------------------------------

# Parameter class -------------------------------------------------------
		
class Parameter:
	'''
	Purpose: 
		The class represents the Parameter element of the parameter file
	Instance variables:
		label: the label of the individual Parameter element 
		val: the value of the individual Parameter element 
	Methods:
		__inti__(self, label, value=None):
			the constructor of the Parameter object for initiation, with four 
			arguments: 
				label, the label of the Parameter; 
				val, the value of the Parameter;
			that initiate the label, parent and the stored value of the Parameter 
			object
		getValue(self): 
			print out the type of the value of the individual parameter and return 
			the stored value, without argument
		setValue(self, val):
			set the new value to the val variable with argument val
		__repr___(self):
			return the string that represents the stored value
		writeOutString(self, depth):
			return the string for writting out with argument depth, the string of 
			spaces that represents the level of the Parameter element
		returnData(self):
			return the exact value of the Parameter object stored as the Value object
	'''
	def __init__(self, label, val):
		self.label = label
		if type(val) is list:
			self.val = val
		else:
			self.val = Value(val)

	def getValue(self):
		print(self.val.getType())
		return self.val.getValue()

	def setValue(self, val):
		if type(val) is list:
			if val[0] is list:
				raise Exception('Not valid input for Parameter.')
			self.val = []
			for i in range(len(val)):
				self.val.append(Value(str(val[i])))
		else:
			self.val = Value(str(val))

	def __repr__(self):
		if type(self.val) is list:
			v = []
			for i in range(len(self.val)):
				v.append(self.val[i].getValue())
			return str(v)
		else:
			return str(self.val.getValue())

	def writeOutString(self, depth=''):
		s = ''
		if type(self.val) is list:
			s += depth + f'{self.label:40}'
			s += f'{self.val[0].getValue():>6}'
			for i in range(1, len(self.val)):
				s += f'{self.val[i].getValue():>7}'
			s += '\n'
		else:
			s += depth + f'{self.label:20}'
			if self.val.getType() is float:
				v = f'{self.val.getValue():.12e}'
				s += f'{v:>20}\n'
			else:
				s += f'{self.val.getValue():>20}\n'
		return s

	def returnData(self):
		if type(self.val) is list:
			v = []
			for i in range(len(self.val)):
				v.append(self.val[i].getValue())
			return v
		else:
			return self.val.getValue()

# End class Parameter ---------------------------------------------------

# Array class -----------------------------------------------------------

class Array:
	'''
	Purpose:
		The class represents the Array element of the parameter file
	Instance variables:
		label: the label of the Array element
		value: the value of the Array element, defult to be an empty list
	Methods:
		__inti__(self, label, openFile, val=None):
			the constructor of the Array object for initiation, with four 
			arguments: 
				label, the label of the Array; 
				openFile, the opened parameter file;
				val, the value of the Array, defult to be None;
			that initiate the label and the parent of the Array object, and 
			pass in the open file for reading
		read(self, openFile):
			method to read the open parameter file, openFile as the argement, line 
			by line and update the value variable according to the read lines;
			reading stop when ']' is read
		__repr__(self):
			return the string of the value variable, in the list format string 
		writeOutString(self, depth):
			return the string for writting out with argument depth, the string of 
			spaces that represents the level of the Array element
		returnData(self):
			return the list of exact value of the Array object stored as the 
			Value object
		setValue(self, val):
			set new value to the val variable with argement val
	'''
	def __init__(self, label, openFile, val=None):
		self.label = label
		if val == None:
			self.val = []
		else:
			self.val = val
		if openFile != None:
			self.read(openFile)

	def read(self, openFile):
		line = openFile.readline()
		l = line.split()
		while l[0] != ']':
			if len(l) == 1:
				self.val.append(Value(l[0]))
			else:
				ls = []
				for i in range(len(l)):
					ls.append(Value(l[i]))
				self.val.append(ls)

			line = openFile.readline()
			l = line.split()

	def __repr__(self):
		v = []
		if type(self.val[0]) is list:
			for i in range(len(self.val)):
				v.append([])
				for j in range(len(self.val[0])):
					v[i].append(self.val[i][j].getValue())
		else:
			for i in range(len(self.val)):
				v.append(self.val[i].getValue())
		return str(v)

	def writeOutString(self, depth=''):
		s = ''
		s += depth + self.label + '[' + '\n'
		if type(self.val[0]) != list:
			for i in range(len(self.val)):
				v = f'{self.val[i].getValue():.12e}'
				s += depth + f'{v:>40}\n'
		else:
			if (self.val[0][0].getType() == int) & (len(self.val[0]) == 2):
				for i in range(len(self.val)):
					v = f'{self.val[i][1].getValue():.12e}'
					s += depth + f'{self.val[i][0].getValue():>41}{v:>22}\n'
			else:
				for i in range(len(self.val)):
					s += depth + f'{self.val[i][0].getValue():^20}'
					for j in range(1, len(self.val[0])):
						if j == (len(self.val[0])-1):
							if self.val[i][j].getValue() < 0:
								v = f'{self.val[i][j].getValue():.11e}'
							else:
								v = f'{self.val[i][j].getValue():.12e}'
							s += f'{v:>22}\n'
						elif j == 1:
							s += f'{self.val[i][j].getValue()}'
						else:
							s += f'{self.val[i][j].getValue():>5}'
		s += depth + ']\n'
		return s

	def returnData(self):
		v = []
		if type(self.val[0]) is list:
			for i in range(len(self.val)):
				v.append([])
				for j in range(len(self.val[0])):
					v[i].append(self.val[i][j].getValue())
		else:
			for i in range(len(self.val)):
				v.append(self.val[i].getValue())
		return v

	def setValue(self, val):
		if (type(val) is list) == False:
			raise Exception('Not valid input for Array.')
		else:
			v = []
			if type(val[0]) is list:
				same = True
				for i in range(len(val)):
					if len(val[i]) != 1:
						same = False
						break
				if same == True:
					for i in range(len(val)):
						v.append(Value(str(val[i][0])))
				else:
					for i in range(len(val)):
						v.append([])
						for j in range(len(val[i])):
							v[i].append(Value(str(val[i][j])))
			else:
				for i in range(len(val)):
					v.append(Value(str(val[i])))
			self.val = v


# End class Array -------------------------------------------------------

# Matrix class ----------------------------------------------------------

class Matrix:
	'''
	Purpose:
		The class represents the Matrix element of the parameter file
	Instance variables:
		label: the label of the Matrix element
		value: the value of the Matrix element, defult to be an empty list
	Methods:
		__inti__(self, label, openFile):
			the constructor of the Matrix object for initiation, with four 
			arguments: 
				label, the label of the Matrix; 
				openFile, the opened parameter file;
			that initiate the label and the parent of the Matrix object, and 
			pass in the open file for reading
		read(self, openFile):
			method to read the open parameter file, openFile as the argement, line 
			by line and update the value variable according to the read lines;
			reading stop when ')' is read
		__repr__(self):
			return the string of the value variable, in the list format string 
		writeOutString(self, depth):
			return the string for writting out with argument depth, the string of 
			spaces that represents the level of the Matrix element
		returnData(self):
			return the list of exact value of the Matrix object stored as the 
			Value object
		setValue(self, val):
			set new value to the val variable with argement val
	'''

	def __init__(self, label, openFile):
		self.label = label
		self.val = []
		self.read(openFile)

	def read(self, openFile):
		att = []
		line = openFile.readline()
		l = line.split()
		while l[0] != ')':
			att.append(l)
			line = openFile.readline()
			l = line.split()
		rowMax = att[0][0]
		colMax = att[0][1]
		for i in range(1, len(att)):
			if att[i][0] > rowMax:
				rowMax = att[i][0]
			if att[i][1] > colMax:
				colMax = att[i][1]
		size = int(max(rowMax, colMax))+1
		for i in range(0, size):
			self.val.append([])
			for j in range(0, size):
				self.val[i].append(Value('0'))
		for i in range(0, len(att)):
			self.val[int(att[i][0])][int(att[i][1])] = Value(att[i][2])
			self.val[int(att[i][1])][int(att[i][0])] = Value(att[i][2])

	def __repr__(self):
		v = []
		for i in range(len(self.val)):
			v.append([])
			for j in range(len(self.val[0])):
				v[i].append(self.val[i][j].getValue())
		return str(v)

	def writeOutString(self, depth=''):
		s = ''
		s += depth + self.label + '(\n'
		for i in range(len(self.val)):
			for j in range(i+1):
				s += depth + f'{i:>24}{j:>5}   ' + f'{self.val[i][j].getValue():.12e}\n'
		s += depth + ')\n'
		return s

	def returnData(self):
		v = []
		for i in range(len(self.val)):
			v.append([])
			for j in range(len(self.val[0])):
				v[i].append(self.val[i][j].getValue())
		return v

	def setValue(self, val):
		if type(val) != list:
			raise TypeError('This is not a valid value for Matrix.')
		else:
			if type(val[0]) is list: # input value is a matrix
				if len(val) != len(val[0]):
					raise Exception('Input Matrix should be squared.')
				for i in range(len(val)):
					for j in range(i):
						if val[i][j] != val[j][i]:
							raise Exception('This is not a diagonal symmetric squared Matrix.')
				for i in range(len(val)):
					if val[i][i] != 0:
						raise Exception('The diagonal of the Matrix should all be zero.')
				self.val = []
				for i in range(len(val)):
					self.val.append([])
					for j in range(len(val[0])):
						self.val[i].append(Value(str(val[i][j])))
			else: # input value is a list in format: [x-index, y-index, value]
				if len(val) != 3:
					raise Exception('Not valid input format for Matrix modification.')
				elif (type(val[0]) != int) or (type(val[1]) != int) or ((type(val[-1]) != int) and (type(val[-1]) != float)):
					raise Exception('Not valid input format for Matrix modification.')
				self.val[val[0]][val[1]] = Value(str(val[-1]))
				self.val[val[1]][val[0]] = Value(str(val[-1]))

# End class Matrix ------------------------------------------------------

# Test 1 ---------------------------------------------------------------
p = Composite('param.cs1')
print(p)
p.writeOut('cs1out')
print(p.Sweep.parameters)
print(p.Sweep.parameters[0])
p.Mixture.Polymer[1].phi *= 2
print(p.Mixture.Polymer[1].phi)
p.Interaction.chi = [1, 0, 0.8]
print(p.Interaction.chi)
p.Mixture.monomers = [[2.0],[2.0]]
print(p.Mixture.monomers)
print(p)

# Test 2 ---------------------------------------------------------------

p2 = Composite('param_film')
print(p2)
p2.writeOut('filmOut')
p2.Interaction.chi = [[0, 0.8], [0.8, 0]]
print(p2)
