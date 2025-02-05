# %%
def binary_dict():
  # list of number
  numbers_to_binary = list(range(0,16))

  #list of binary numbers
  binaries = []
  #loop over base 10 numbers, apply bin() to each
  for number_base_10 in numbers_to_binary:

  # loop over numbers
    # apply bin
    binary_nums = bin(number_base_10)

    #add thenm to list
    binaries.append(binary_nums[2:])

    #zip together and convert

  return dict(zip(numbers_to_binary, binaries))

zipped_list = binary_dict()
zipped_list
