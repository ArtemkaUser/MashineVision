class Person:
    name = 'Ivan'
    age = 10

    def set(self, name, age):
        self.name = name
        self.age = age


class Student(Person):
    course = 1


igor = Student()
igor.set("igor", 19)
print(igor.name)
vlad = Person()
vlad.set("Vlad", 25)
print(vlad.name + " " +str(vlad.age))
