class SortedList(list):
  '''
  override .append() function to sort list after append
  '''
  def append(self,value):
    super().append(value)
    self.sort()

class MissingObjectsOfDictClass(dict):
  def get_key(self,key):
    """
    get_key() - if key doesn't exist it will return available keys

    """
    if key in self:
       return key
    else:
      return f'"{key}" not found, Available {super().keys()}'
      
  def searh_by_value(self,search_value):
    '''
    search dict by value and return it's key
    '''
    for k,v in super().items():
      if search_value in v:
        return f'key of {search_value} is  {k}'
    else:
      return 'Not Found'
