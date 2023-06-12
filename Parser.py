
'''
File Contents:
	class Element:
		The Element class is the base class of all types of elements in the parameter
		file. It has four subclasses: Composite, Parameter, Array and Matrix.
	class Value:
		A Value object stores the value of a single string that represents all or part
		part of the value of a parameter. It could implement code to figure out the 
		type of values among string, integer and floating point.
	class Composite(Element):
		A Composite object can be identified by opening and closing curly brackets
		('{' and '}'). It can parse a parameter file block and store its contents
		in a form that allows particular types of items within it to be accessed 
		and modified.
	class Parameter(Elememt):
		A Parameter object contains a parameter label and its value for the individual 
		parameter within a single line.
	class Array(Element):
		An Array object is a type of parameter that has values stored as elements of
		a one-dimensional array which is given in a multi-line format in which the
		first row contains a label that contains the name of the array followed 
		immediately by an opening square bracket ('['') and the last line contains a 
		matching closing square bracket (']') itself. Elements of the
		one-dimentional array are in between these delimiters with one element per
		line and appear in order of increasing array index started from 0. 
	class Matrix(Element):
		A Matrix object is a type of parameter that has values stored as elements of
		a matrix or two-dimentional array in element format that the value of each
		nonzero element of the matrix appears on separate line. The element format 
		for a matrix starts with a line that contains a name label followed 
		immediately by an opening parenthesis and ends with a line contains a matching 
		closing paranthesis itself. In between, each line contains a row index, a 
		column index and value of a single element of the array. 
	def readParamFile(filename):
		A method to read the parameter file with specific filename and store the data
		of all parameters in the read file
	
'''

# Element class --------------------------------------------------------------------

class Element:
	'''
	Purpose: 
		The base class of all types of elements of the parameter file, with four
		subclasses:
			Composite: 
				Parameter block identified by opening and closing curly brackets 
				('{' and '}')
			Parameter: 
				Single value parameter within a single line
			Array: 
				Parameter has values stores in an one-dimentional array identified 
				by openning and closing square brakets ('[' and ']')
			Matrix:
				Parameter has values stores in a two-dimentional array (matrix)
				identified by openning and closing parenthesis
	Instance variables:
		label: Element label of the parameter file
		parent: The parent of the element, defult to be None
	Methods:
		__inti__(self, label, openFile=None, parent=None, value=None):
			The constructor of the Element object for initiation, with four 
			arguments: 
				label, the label of the Element; 
				openFile, file name of the opened parameter file, defult to be None;
				parent, the parent of the Elment, defult to be None;
				value, the value of the Element, defult to be None;
			that initiate the label and the parent of the Element object
		getLabel(self): 
			return the label of the element
	'''
	def __init__(self, label, openFile=None, parent=None, value=None):
		self.label = label
		self.parent = parent

	def getLabel(self):
		return self.label

# End class Element ----------------------------------------------------------------

# Value class ----------------------------------------------------------------------	

class Value:
	'''
	Purpose: 
		The class represents the object type that store the single value for parameters 
		of the parameter file by distinguishing the exact type of it
	Instance variables:
		value: variable to store a single value of the parameters
		type: the type of the value stored, either integer, floating point or string
	Methods:
		getType(self): return the type of stored value
		getValue(self): return the value of stored value
	Note:
		Debugging by the commented line to check if the constructor has the expected 
		function of distinguishing the exact type of the value

	'''
	def __init__(self, value):
		if value.isdigit() == True:
			# print('int')
			self.value = int(value)
		else:
			try:
				self.value = float(value)
				# print('float')
			except ValueError:
				self.value = value
				# print('string')
		# print(self.value)
		self.type = type(self.value)

	def getType(self):
		return self.type

	def getValue(self):
		return self.value

# End class Value ---------------------------------------------------------

# Composite class ---------------------------------------------------------

class Composite(Element):
	'''
	Purpose:
		The class represents the Copmosite element of the parameter file, which
		is a subclass of the Element class
	Instance variables:
		label: the label of the Composite element 
		parent: the parent of the current Composite element 
		children: 
			the children items of the Composite in the parameter file, defult 
			to be an empty dictionary
	Methods:
		__inti__(self, label, openFile=None, parent=None, value=None):
			the constructor of the Composite object for initiation, with four 
			arguments: 
				label, the label of the Composite; 
				openFile, the open parameter file;
				parent, the parent of the current Composite, defult to be None;
				value, the value of the Composite, defult to be None;
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
	'''
	def __init__(self, label, openFile, parent=None, value=None):
		super().__init__(label, openFile, parent, value)
		# self.children = [] # Need to be changed to dictionary in order to use dot notation
		self.children = {} # Dictionary is used for dot natation
		self.read(openFile)

	def read(self, openFile):
		line = openFile.readline()
		l = line.split()
		# print(line, end='')
		while line != '':
			if l[0][-1] == '{':
				p = Composite(l[0][:-1], openFile, self, None)
			elif l[0][-1] == '[':
				if len(l) == 1:
					p = Array(l[0][:-1], openFile, self, None)
				else:
					value = []
					if l[-1] == ']':
						for i in range(1, len(l)-1):
							value.append(Value(l[i]))
						p = Array(l[0][:-1], None, self, value)
					else:
						for i in range(1,len(l)):
							value.append(Value(l[i]))
						p = Array(l[0][:-1], openFile, self, value)	
			elif l[0][-1] == '(':
				p = Matrix(l[0][:-1], openFile, self, None)
			elif l[0] == '}':
				break
			else:
				if len(l) == 2:
					p = Parameter(l[0], None, self, l[1])
				else:
					# print('This is not a valid line.')
					value = []
					for i in range(1, len(l)):
						value.append(Value(l[i]))
					p = Parameter(l[0], None, self, value)
			self.addChild(p)	
			line = openFile.readline()
			l = line.split()
			# print(line, end='')

	def addChild(self, child):
		# self.children.append(child) # Need to be changed because children will be changed to dictionary
		label = child.getLabel()
		if label in self.children:
			self.children[label] = [self.children[label]]
			self.children[label].append(child)
		else:
			self.children[label] = child

	def getChildren(self):
		return self.children

	def __repr__(self):
		return str(self.children)

	def __getattr__(self, attr):
		if type(self.children[attr]) is Parameter:
			if type(self.children[attr].value) is list:
				return self.children[attr].value
			else:
				return self.children[attr].value.value
		else:
			return self.children[attr]

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

		


# End class Composite ---------------------------------------------------

# Parameter class -------------------------------------------------------
		
class Parameter(Element):
	'''
	Purpose: 
		The class represents the Parameter element of the parameter file, which
		is a subclass of the Element class
	Instance variables:
		label: the label of the individual Parameter element 
		parent: the parent of the current individual Parameter element 
		value: the value of the individual Parameter element 
	Methods:
		__inti__(self, label, openFile=None, parent=None, value=None):
			the constructor of the Parameter object for initiation, with four 
			arguments: 
				label, the label of the Parameter; 
				openFile, the open parameter file, defult to be None;
				parent, the parent of the current Parameter, defult to be None;
				value, the value of the Parameter;
			that initiate the label, parent and the stored value of the Parameter 
			object
		getValue(self): 
			print out the type of the value of the individual parameter and return 
			the stored value, without argument
		setValue(self, value):
			set the new value to the value variable with argument value
		__repr___(self):
			return the string that represents the stored value
		writeOutString(self, depth):
			return the string for writting out with argument depth, the string of 
			spaces that represents the level of the Parameter element
	'''
	def __init__(self, label, openFile=None, parent=None, value=None):
		super().__init__(label, openFile, parent, value)
		if type(value) is list:
			self.value = value
		else:
			self.value = Value(value)

	def getValue(self):
		print(self.value.getType())
		return self.value.getValue()

	def setValue(self, value):
		self.value = Value(str(value))

	def __repr__(self):
		if type(self.value) is list:
			v = []
			for i in range(len(self.value)):
				v.append(self.value[i].getValue())
			return str(v)
		else:
			return str(self.value.getValue())

	def writeOutString(self, depth):
		s = ''
		if self.label == 'mesh':
			s += depth + f'{self.label:40}'
			if type(self.value) is list:
				s += f'{self.value[0].getValue():>6}'
				for i in range(1, len(self.value)):
					s += f'{self.value[i].getValue():>7}'
				s += '\n'
			else:
				s += f'{self.value.getValue():>6}\n'
		else:
			s += depth + f'{self.label:20}'
			if self.value.getType() is float:
				v = f'{self.value.getValue():.12e}'
				s += f'{v:>20}\n'
			else:
				s += f'{self.value.getValue():>20}\n'
		return s

# End class Parameter ---------------------------------------------------

# Array class -----------------------------------------------------------

class Array(Element):
	'''
	Purpose:
		The class represents the Array element of the parameter file, which
		is a subclass of the Element class
	Instance variables:
		label: the label of the Array element
		parent: the parent of the current Array element
		value: the value of the Array element, defult to be an empty list
	Methods:
		__inti__(self, label, openFile=None, parent=None, value=None):
			the constructor of the Array object for initiation, with four 
			arguments: 
				label, the label of the Array; 
				openFile, the opened parameter file;
				parent, the parent of the current Array, defult to be None;
				value, the value of the Array, defult to be None;
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
	'''
	def __init__(self, label, openFile=None, parent=None, value=None):
		super().__init__(label, openFile, parent, value)
		if value == None:
			self.value = []
		else:
			self.value = value
		if openFile != None:
			self.read(openFile)

	def read(self, openFile):
		line = openFile.readline()
		l = line.split()
		# print(line, end='')
		while l[0] != ']':
			if len(l) == 1:
				self.value.append(Value(l[0]))
			else:
				ls = []
				for i in range(len(l)):
					ls.append(Value(l[i]))
				self.value.append(ls)

			line = openFile.readline()
			l = line.split()
			# print(line, end='')

	def __repr__(self):
		v = []
		if type(self.value[0]) is list:
			for i in range(len(self.value)):
				v.append([])
				for j in range(len(self.value[0])):
					v[i].append(self.value[i][j].getValue())
		else:
			for i in range(len(self.value)):
				v.append(self.value[i].getValue())
		return str(v)

	def writeOutString(self, depth):
		s = ''
		s += depth + self.label + '[' + '\n'
		if type(self.value[0]) != list:
			for i in range(len(self.value)):
				v = f'{self.value[i].getValue():.8e}'
				s += depth + f'{v:>35}\n'
		else:
			if (self.value[0][0].getType() == int) & (len(self.value[0]) == 2):
				for i in range(len(self.value)):
					v = f'{self.value[i][1].getValue():.12e}'
					s += depth + f'{self.value[i][0].getValue():>41}{v:>22}\n'
			else:
				for i in range(len(self.value)):
					s += depth + f'{self.value[i][0].getValue():^20}'
					for j in range(1, len(self.value[0])):
						if j == (len(self.value[0])-1):
							if self.value[i][j].getValue() < 0:
								v = f'{self.value[i][j].getValue():.11e}'
							else:
								v = f'{self.value[i][j].getValue():.12e}'
							s += f'{v:>22}\n'
						elif j == 1:
							s += f'{self.value[i][j].getValue()}'
						else:
							s += f'{self.value[i][j].getValue():>5}'
		s += depth + ']\n'
		return s


# End class Array -------------------------------------------------------

# Matrix class ----------------------------------------------------------

class Matrix(Element):
	'''
	Purpose:
		The class represents the Matrix element of the parameter file, which
		is a subclass of the Element class
	Instance variables:
		label: the label of the Matrix element
		parent: the parent of the current Matrix element
		value: the value of the Matrix element, defult to be an empty list
	Methods:
		__inti__(self, label, openFile=None, parent=None, value=None):
			the constructor of the Matrix object for initiation, with four 
			arguments: 
				label, the label of the Matrix; 
				openFile, the opened parameter file;
				parent, the parent of the current Matrix, defult to be None;
				value, the value of the Matrix, defult to be None;
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
	'''

	def __init__(self, label, openFile=None, parent=None, value=None):
		super().__init__(label, openFile, parent, value)
		self.value = []
		self.read(openFile)

	def read(self, openFile):
		att = []
		line = openFile.readline()
		l = line.split()
		# print(line, end='')
		while l[0] != ')':
			att.append(l)
			line = openFile.readline()
			l = line.split()
			# print(line, end='')
		rowMax = att[0][0]
		colMax = att[0][1]
		for i in range(1, len(att)):
			if att[i][0] > rowMax:
				rowMax = att[i][0]
			if att[i][1] > colMax:
				colMax = att[i][1]
		size = int(max(rowMax, colMax))+1
		for i in range(0, size):
			self.value.append([])
			for j in range(0, size):
				self.value[i].append(Value('0'))
		for i in range(0, len(att)):
			self.value[int(att[i][0])][int(att[i][1])] = Value(att[i][2])
			self.value[int(att[i][1])][int(att[i][0])] = Value(att[i][2])

	def __repr__(self):
		v = []
		for i in range(len(self.value)):
			v.append([])
			for j in range(len(self.value[0])):
				v[i].append(self.value[i][j].getValue())
		return str(v)

	def writeOutString(self, depth):
		s = ''
		s += depth + self.label + '(\n'
		for i in range(len(self.value)):
			for j in range(i+1):
				s += depth + f'{i:>24}{j:>5}   ' + f'{self.value[i][j].getValue():.12e}\n'
		s += depth + ')\n'
		return s

# End class Matrix ------------------------------------------------------

# readParamFile(filename) Method ----------------------------------------

def readParamFile(filename):
	'''
	Argument:
		filename: string, name of the specific parameter file needed to be read
	Return:
		the 'System' composite of the read parameter file
	Note:
		'This is not a valid parameter file.' will be print if the read file were
		not in the correct format and return None
	'''
	with open(filename) as f:
		firstLine = f.readline()
		# print(firstLine, end='')
		if firstLine != "System{"+'\n':
			p = None
			print('This is not a valid parameter file.')
		else:
			# line = f.readline()
			# l = line.split()
			# p = Composite(l[0][:-1], f, None, None)
			p = Composite('System', f, None, None)
	return p

# End Method -----------------------------------------------------------

# Test 1 ---------------------------------------------------------------

p = readParamFile('param.cs1') 
print(p)
print(p.Mixture.Polymer[1].phi)
print(p.Mixture.Polymer[1].phi*2)
print(p)
print(p.Sweep.parameters)
p.writeOut('cs1out')

# Test 2 ---------------------------------------------------------------

p2 = readParamFile('param100')
print(p2)
print(p2.Domain)

# Test 3 ---------------------------------------------------------------

print(readParamFile('test')) 

# Test 4 ---------------------------------------------------------------

p3 = readParamFile('param2.cs1')
print(p3)
print(p3.Mixture.monomers)

# Test 5 ---------------------------------------------------------------

p4 = readParamFile('param3.cs1')
print(p4)
print(p4.Mixture.monomers)

# Test 6 ---------------------------------------------------------------

p5 = readParamFile('param_tri')
print(p5)
p5.writeOut('triOut')

# Test 7 ---------------------------------------------------------------

p6 = readParamFile('param_solv')
print(p6)
p6.writeOut('solvOut')

# Test 8 ---------------------------------------------------------------

p7 = readParamFile('param50down')
print(p7)
p7.writeOut('50downOut')
