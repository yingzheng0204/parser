
'''
File Contents:
	class Element:
		The Element class is the base class of all types of elements in the parameter
		file.
	class Value:
		A Value object stores the value of a single string that represents all or part
		part of the value of a parameter. It could implement code to figure out the 
		type of values among string, integer and floating point.
	class Composite(Element):
		A Composite object can be identified by opening and closing curly brackets
		("{" and "}"). It can parse a parameter file block and store its contents
		in a form that allows particular types of elements within it to be accessed 
		and modified.
	class Parameter(Elememt):
		A Parameter object contains a parameter label and its value within a single
		line.
	class Array(Element):
		An Array object is a type of parameter that has values stored as elements of
		a one-dimensional array which is given in a multi-line format in which the
		first row contains a label that contains the name of the array followed 
		immediately by an opening square bracket ("[") and the last line contains a 
		matching closing square bracket ("]") itself. Elements of the
		one-dimentional array are in between these delimiters with one element per
		line and appear in order of increasing array index started from 0. 
	class Matrix(Element):
		A Matrix object is a type of parameter that has values stored as elments of
		a matrix or two-dimentional array in element format that the value of each
		nonzero element of the matrix appears on separate line. The element format 
		for a matrix starts with a line that contains a name label followed 
		immediately by an opening parenthesis and ends with a line contains a matching 
		closing paranthesis itself. In between, each line contains a row index, a 
		column index and value of a single element of the array. 
	def readParamFile(filename):
		A method to read the parameter file with specific filename
	
'''

class Element:
	'''
	Purpose: The base class of all types of elements in the parameter file
	Instance variables:
		label: Element label in the parameter file
		parent: Parent object of the element, defult to be None
		children: Children object of the element, defult to be empty list
	Methods:
		read(self, filename, pos): 
		match():
	'''
	def __init__(self, label, parent=None):
		self.label = label
		self.parent = parent
		self.children = []

	def read(self, openFile):
		line = openFile.readline()
		while line != '':
			if line[-2] == '{':
				p = Composite(line[:-2], self)
				addChild(p)
			elif line[-2] == '[':
				p = Array(line[:-2], self)
				addChild(p)
			elif line[-2] == '(':
				p = Matrix(line[:-2], self)
				addChild(p)
			else:
				p = Parameter(line[:line.find(' ')], self, Value(line[line.rfind(' ')+1 : -1]))
				addChild(p)




	# def match(self):

	def addChild(self, child):
		self.children.append(child)

class Value:
	'''
	Purpose: The object type to store values for parameters
	Instance variables:
	Methods:
	'''
	def __init__(self, value):
		if value.isnumeric() == True:
			# print('int')
			self.value = int(value)
		elif value.find('.') != -1:
			# print('float')
			self.value = float(value)
		else:
			# print('string')
			self.value = value
		# print(self.value)

	# def __repr__(self):
	# 	return self.value

	def getType(self):
		return type(self.value)

	def getValue(self):
		return self.value

class Composite(Element):
	'''
	Purpose:
	Instance variables:
	Methods:
	'''
	def __init__(self, label, parent=None):
		super().__init__(self, label, parent)


	# def read(self, openFile):

	def getComposite(self):
		print(self.children)


		
class Parameter(Element):
	'''
	'''
	def __init__(self, label, parent, value):
		self.label = label
		self.parent = parent
		self.value = value

	def getValue(self):
		print(self.value.getType())
		return self.value.getValue()

# End class Parameter -----------------------------------


class Array(Element):
	'''
	'''

class Matrix(Element):
	'''
	'''

def readParamFile(filename):
	with open(filename) as f:
		firstLine = f.readline()
		if firstLine != "System{"+'\n':
			print('This is not a valid parameter file.')
		else:
			p = Composite('System')
			p.read(filename)


# readParamFile('param100')

# line = 'ds                    5.000000000000e-02\n'
# # print(line[:line.find(' ')])
# # print(line.rfind(' '))
# # print(line[line.rfind(' ')+1 : -1])
# p = Parameter(line[:line.find(' ')], None, Value(line[line.rfind(' ')+1 : -1]))
# print(p.getValue())
