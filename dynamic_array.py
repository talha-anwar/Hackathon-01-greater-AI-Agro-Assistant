import ctypes

class Mylist:
  def __init__(self):
    self.size = 1
    self.n = 0
    # creates a C type array with size = self.size
    self.A = self.__create_array(self.size)

  def __create_array(self, capacity):
    # creates a C type array (static, referencial) with size capacity 
    return (capacity*ctypes.py_object)()

  def append(self, item):
    if self.size == self.n:
      # resize

    self.A[self.n] = item
    
    
  def __len__(self, length):
    return self.n

L = Mylist()
