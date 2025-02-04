
alphabet = "abcdefghijklmnopqrstuvwxyz"

def index_return(target):
  return list(enumerate(target))

# to store list as a variable -- needs to be outside of the function

indexed_list = index_return(alphabet)

# display vs print are different

display(indexed_list)
print(indexed_list)
