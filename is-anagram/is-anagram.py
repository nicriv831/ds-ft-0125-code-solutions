# %%
str1 = 'roots'
str2 = 'torso'
str3 = 'hello'

def is_anagram(first_ana, second_ana):
  first_ana_sorted = ''.join(sorted(first_ana))
  second_ana_sorted = ''.join(sorted(second_ana))
  if first_ana_sorted == second_ana_sorted:
    return True
  else:
    return False

# %%
print('Roots and torso are anagram?', is_anagram(str1, str2))

# above works correctly with str1 and 2, this one is a sanity check for "False" with str2 and str3

print('Torso and hello are anagram?', is_anagram(str1, str3))
