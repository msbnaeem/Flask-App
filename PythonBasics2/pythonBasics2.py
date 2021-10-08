from collections import Counter
# Python Activity
#
# Fill in the code for the functions below.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code. Make sure to add what is going to be returned.


# Part A (count_threes) now needs to return the multiple
# of three that occurs the most in a string. For example,
# 0939639 would return 9 since it appeared 3 times while the other multiple of three appeared less than that.
# You only need to worry about single digit multiples of 3 (3, 6, 9). You must use a dictionary to accomplish this.

def count_threes(n):
  # YOUR CODE HERE
  # Initiated counter with the following keys and values
  counter = {3: 0, 6: 0, 9: 0}
  # iteration in n
  for i in n:
    #  type casting i to int
    i = int(i)
    # checks for remainder to be 0 and then gets incremented if 0
    if (i != 0) and (i % 3) == 0:
      # keys are getting incremented
      counter[i] += 1
  #  comparing 3 with 6 and 9 and then returns 3
  if (counter[3] >= counter[6]) and  (counter[3] >= counter[9]):
    return 3
  # comparing 6 and 9 and then returns 6
  elif (counter[6] >= counter[9]):
    return 6
  # lastly jut gets returned if none of the above happens
  else:
    return 9


# Part B (longest_consecutive_repeating_char) now needs to account
# for the edge case where two characters have the same consecutive repeat length.
# The return value should now be a list containing all characters with the longest consecutive repeat. For example,
# the longest_consecutive_repeating_char('aabbccd') would return ['a', 'b', 'c'] (order doesn't matter).
# You must use a dictionary to accomplish this.

def longest_consecutive_repeating_char(s):
  # YOUR CODE HERE
  counter = {}
  count = 1
  lcr = -1
  # iteration to check and determine whether the character in counter is present and increments the dictionary,
  # if not then adds it in to the dictionary
  for i in range(0, len(s) - 1):
    # checks the equality of first and next element in the s
    if s[i] != s[i + 1]:
      # checking the element in s is in counter dictionary and is greater than the count then it continues
      if (s[i] in counter) and (counter[s[i]] > count):
        continue
      #  else sets index of in dictionary to the count then resets it
      else:
        counter[s[i]] = count
        count = 1
    # if first and next element matches then increments
    else:
      count += 1
  counter[s[len(s) - 1]] = count

  # finiding logest consecutive repeating char by iteration
  for k, v in counter.items():
    if v > lcr:
      lcr = v
  # myList code begins
  myList = []
  # items gets added into myList in order to return the list of characters with iteration
  for k, v in counter.items():
    if v == lcr:
      myList.append(k)
  return myList





# Part C. is_palindrome
# Define a function is_palindrome(s) that takes a string s
# and returns whether or not that string is a palindrome.
# A palindrome is a string that reads the same backwards and
# forwards. Treat capital letters the same as lowercase ones
# and ignore spaces (i.e. case insensitive).
def is_palindrome(s):
  # YOUR CODE HERE
  s = s.lower().replace(" ", "")
  for i in range(0, int(len(s)/2)):
    if s[i] != s[len(s) - i - 1]:
      return False
  return True


