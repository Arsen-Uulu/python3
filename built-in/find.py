def find(search_from,argument):
  arg_possition = 0 
  for index in range(len(search_from)):
    if argument[0] in search_from[index]:
      arg_possition = index
  return arg_possition
