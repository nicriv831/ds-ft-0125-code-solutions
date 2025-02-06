# %%
#Letters to Symbols

#need to use itertools to use groupby which will make groups based on consecutive letters
import itertools as it

# %%
# list that we will eventually "encode"
s ='AAAABBBCCDAAA'

# %%
def letters_to_symbols(letters):

    # this will loop through each letter and make separate groups for each letter as an object
    # len(list(group)) gives us the length of the group, {letter} adds the letter to the end, the for loop at the end then loops back to the next group and repeats

    result = ''.join(f"{len(list(group))}{letter}" for letter, group in it.groupby(letters))
    return result

# %%
letters_to_symbols(s)
