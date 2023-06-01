
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
		label: The label of the Composite element of the parameter file
		parent: The parent of the current Composite element in the parameter file
		children: 
			The children items of the Composite in the parameter file, defult 
			to be an empty dictionary
	Methods:
		__inti__(self, label, openFile=None, parent=None, value=None):
			The constructor of the Composite object for initiation, with four 
			arguments: 
				label, the label of the Composite; 
				openFile, file name of the opened parameter file;
				parent, the parent of the Composite, defult to be None;
				value, the value of the Composite, defult to be None;
			that initiate the label and the parent of the Composite object, and 
			pass in the open file for reading
		read(self, openFile):
			method to read the open parameter file, openFile as the argement, line 
			by line and add the read items into the children variable
		addChild(self, child):
			method to add the single item, argument child, into the children variable
		



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
			if len(l) == 1:
				if l[0][-1] == '{':
					p = Composite(l[0][:-1], openFile, self, None)
					self.addChild(p)
				if l[0][-1] == '[':
					p = Array(l[0][:-1], openFile, self, None)
					self.addChild(p)
				if l[0][-1] == '(':
					p = Matrix(l[0][:-1], openFile, self, None)
					self.addChild(p)
				if l[0] == '}':
					break
			if len(l) == 2:
				p = Parameter(l[0], None, self, l[1])
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

	def getComposite(self):
		print(self.children)

	def __repr__(self):
		return str(self.children)

	def __getattr__(self, attr):
		return self.children[attr]


# End class Composite ---------------------------------------------------

# Parameter class -------------------------------------------------------
		
class Parameter(Element):
	'''
	Purpose: 
		The object type of individual parameter of the parameter file
	Instance variables:
		label: the label of the individual parameter
		parent: the parent of the individual parameter
		value: the value of the indivisual parameter
	Methods:
		getValue(self): 
			print out the type of the value of the indivisual parameter 
			and return the stored value
	'''
	def __init__(self, label, openFile=None, parent=None, value=None):
		super().__init__(label, openFile, parent, value)
		self.value = Value(value)

	def getValue(self):
		print(self.value.getType())
		return self.value.getValue()

	def __repr__(self):
		return str(self.value.getValue())


# End class Parameter ---------------------------------------------------

# Array class -----------------------------------------------------------

class Array(Element):
	'''
	Purpose:
	Instance variables:
	Methods:
	'''
	def __init__(self, label, openFile=None, parent=None, value=None):
		super().__init__(label, openFile, parent, value)
		self.value = []
		self.read(openFile)

	def read(self, openFile):
		line = openFile.readline()
		l = line.split()
		# print(line, end='')
		while l[0] != ']':
			# if len(l) == 1:
			# 	self.value.append([Value(l[0])])
			# if len(l) == 2:
			# 	self.value.append([Value(l[0]), Value(l[1])])

			ls = []
			for i in range(len(l)):
				ls.append(Value(l[i]))
			self.value.append(ls)

			line = openFile.readline()
			l = line.split()
			# print(line, end='')


	def __repr__(self):
		# s = ''
		# for i in range(len(self.value)):
		# 	for j in range(len(self.value[0])):
		# 		if j == len(self.value[0])-1:
		# 			s = s + str(self.value[i][j].getValue())
		# 		else:
		# 			s = s + str(self.value[i][j].getValue()) + '    '
		# 	if i != len(self.value)-1:
		# 		s = s + '\n'
		# return s

		v = []
		for i in range(len(self.value)):
			v.append([])
			for j in range(len(self.value[0])):
				v[i].append(self.value[i][j].getValue())
		return str(v)



# End class Array -------------------------------------------------------

# Matrix class ----------------------------------------------------------

class Matrix(Element):
	'''
	Purpose:
	Instance variables:
	Methods:
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

	def __repr__(self):
		# s = ''
		# for i in range(0, len(self.value)):
		# 	for j in range(0, len(self.value[0])):
		# 		if j == len(self.value[0])-1:
		# 			s = s + str(self.value[i][j].getValue())
		# 		else:
		# 			s = s + str(self.value[i][j].getValue()) + '    '
		# 	if i != len(self.value)-1:
		# 		s = s + '\n'
		# return s

		v = []
		for i in range(len(self.value)):
			v.append([])
			for j in range(len(self.value[0])):
				v[i].append(self.value[i][j].getValue())
		return str(v)


# End class Matrix ------------------------------------------------------



def readParamFile(filename):
	with open(filename) as f:
		firstLine = f.readline()
		# print(firstLine, end='')
		if firstLine != "System{"+'\n':
			print('This is not a valid parameter file.')
		else:
			# line = f.readline()
			# l = line.split()
			# p = Composite(l[0][:-1], f, None, None)
			p = Composite('System', f, None, None)
			# print(p.getChildren())
			# print(p)
			# p.getComposite()
			# print(p.Mixture.Polymer[1].phi)
	return p


p = readParamFile('param.cs1')
print(p)
print(p.Mixture.Polymer[1].phi)
print(p.Sweep.ns)
# print(readParamFile('param100'))


