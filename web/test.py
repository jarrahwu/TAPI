__author__ = 'jarrah'


class Foo:
    def __init__(self, name="N/A", age=99):
        self.name = name
        self.age = age

    def desc(self):
        print("hello my name is %s, age is %d" % (self.name, self.age))