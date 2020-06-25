'''
HashMap with Separate Chaining using linkedList and Node
'''
from linked_list import Node, LinkedList

class HashMap:
  def __init__(self,size):
    self.size = size
    self.array = [LinkedList() for item in range(self.size)]
  
  def get(self,key):
    array_index = self.compress(self.hash(key))
    list_at_index = self.array[array_index] 
    return type(list_at_index)


  def hash(self,key):
    key_bytes = key.encode()
    hash_code = sum(key_bytes)
    return hash_code
    
  def compress(self,hash_code):
    return hash_code % self.size

  def assign(self,key,value):
    array_index = self.compress(self.hash(key))
    payload = Node([key,value])
    list_at_array = self.array[array_index]
    for item in list_at_array:
      if key == item[0]:
        item[1] = value 
        return
    list_at_array.insert(payload)

  def retrieve(self,key):
     array_index = self.compress(self.hash(key))
     list_at_index = self.array[array_index]
     for item in list_at_index:
       if key == item[0]:
         return item[1]
     return 
