class Person :
	name = "" 
	age = 0 
	def __init__(self, name, age): 
		self.name = name 
		self.age = age 
		
	def getName(self,): 
		return self.name 
		
	def getAge(self,): 
		return self.age 
		
	def getAgeCategory(self,) :
		if( self.age < 0) : 
			return "Некорректный возраст" 
			
		elif( self.age < 13) : 
			return "ребёнок" 
			
		elif( self.age < 18) : 
			return "Подросток" 
			
		elif( self.age < 60) : 
			return "Взрослый" 
			
		else: 
			return "Пожилой" 
			
		
	

class Cat :
	name = "" 
	def __init__(self, name): 
		self.name = name 
		
	def getName(self,): 
		return self.name 
		
	
class Dog :
	name = "" 
	def __init__(self, name): 
		self.name = name 
		
	def getName(self,): 
		return self.name 
		
	


def get(): 
	return name 
	


p = Person("Anna", 24) 
p2 = Person("Vladimir",23) 
print(p.getAgeCategory())
print("Hello, Person!")
if( p.name == "Anna" and p2.name == "Vladimir") : 
	print("Ее зовут Анна")
	print("Его зовут Владимир")
	
if( p2.getAge( ) > p.getAge( )): 
	print(p2.getName() + " старше " + p.getName())
	
else: 
	print(p2.getName() + " младше " + p.getName())
	
cat = Cat("Kitty") 
print("Cat'name - " + cat.getName())
cat.name = "Lili" 
print("Cat'name - " + cat.getName())



