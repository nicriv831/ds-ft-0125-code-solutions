
 s = '(a((kl(mns)t)uvwz)'

 def BracketMatcher(test_string):
  open_count = 0
  close_count = 0
  for character in test_string:
    if character == '(':
      open_count = open_count + 1
    elif character == ')':
      close_count = close_count + 1
  if open_count - close_count != 0:
    return False
  else:
    return True

BracketMatcher(s)
