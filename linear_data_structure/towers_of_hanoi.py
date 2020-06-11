from stack import Stack
print("\nLet's play Towers of Hanoi!!")

stacks = []
left_stack = Stack('Left')
middle_stack = Stack('Middle')
right_stack = Stack('Right')
stacks.append(left_stack)
stacks.append(middle_stack)
stacks.append(right_stack)

num_disks =  int(input(
  '\n How many disks do you want to play?\n'
))
count = 0
while True:
  if num_disks < 3:
    num_disks = int(input(
      "Enter a number greater than or equal to 3\n"
    ))
  break

for i in range(num_disks, 0, -1):
    left_stack.push(i)

num_optimal_moves = 2**num_disks - 1 

print(f'The fastest you can solve this game is in {num_optimal_moves} moves')

def get_input():
  choices = [names.get_name() for names in stacks]
  while True:
    for i in range(len(stacks)):
      name = stacks[i].get_name()
      letter = choices[i]
      print("Enter {0} for {1}".format(name,letter))
    user_input = input()
    if user_input in choices:
      for i in range(len(stacks)):
        if user_input == choices[i]:
          return stacks[i]
    
num_user_moves = 0

while right_stack.get_size() != num_disks:
    print("\n\n\n...Current Stacks...")
    for i in range(len(stacks)):
      stacks[i].print_items()
    while True:
      print("\nWhich stack do you want to move from?\n")
      from_stack = get_input()
      print("\nWhich stack do you want to move to?\n")
      to_stack = get_input()
      if from_stack.is_empty():
        print('\n\nInvalid Move. Try again')
      elif to_stack.is_empty() or from_stack.peek() <= to_stack.peek():
        disk = from_stack.pop()
        to_stack.push(disk)
        num_user_moves += 1
        break  
      else:
        print("\n\nInvalid Move. Try Again!")

print("\n\nYou completed the game in {0} moves, and the optimal number of moves is {1}".
format(num_user_moves,num_optimal_moves))
