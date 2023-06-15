class Test:
	def __init__(self, name):
		self.name = name

	def __setattr__(self, key, value):
		print('setattr called')
		self.__dict__[key] = value

a = Test('a')
print(a.name)
a.age = 2
print(a.age)