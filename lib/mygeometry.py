'''
Module geometry.py
'''
# variables
pi = 3.14159265359
phi = 1.6180

# fonction qui calcule l'aire
def aire(obj):
    if type(obj) == carre:
        return obj.a**2

# definitions de quelques classes
class carre(object):
    def __init__(self,a):
        self.a = a

class triangle(object):
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c