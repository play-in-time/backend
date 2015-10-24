import sys
import numpy as np

""" Solve our version of the knapsack problem:
    Given a set of songs S, with each song s = (w, l), w=weight, l=length
    We want to fit some r subset of S into the interval C.
    Thus, we want:
      - L1_norm(r_W) to be maximised
      - L1_norm(r_L) <= C (i.e. to fit within the constraint)

    Parameters:
      weights: an n-vector of song weights, with weights[i] <=> song[i]
      lengths: an n-vector of song lengths, with lengths[i] <=> song[i]
      n: The number of songs in the set S
      C: The time constraint/length of the time interval to work within

    returns: A set of song indices which optimises the problem statent.
"""
def knapsack(weights, lengths, n, C):
  # Initialise matrices to n+1 x C+1 matrices of zeros:
  B = np.zeros((n + 1, C + 1), np.int64, 'C') # 64-bit ints, row-major ordering
  keep = np.zeros((n + 1, C + 1), np.int8, 'C') # 8-bit ints, row-major

  for i in xrange(1, n+1):
    for l in xrange(0, C+1):
      l_i = lengths[i - 1] # treat lengths as 1-indexed
      term1 = B[(i - 1), l]
      term2 = B[(i - 1), (l - lengths[i-1])%(C+1)] + weights[i-1]
      if (lengths[i-1] <= l) and (term2 > term1):
        B[i, l] = term2
        keep[i, l] = 1 # keep this song at this time
      else: # lengths[i] > l and term1 <= term2
        B[i, l] = term1
      
  k = C # Start at last column
  solution = [] # Our solution set
  for i in xrange(n, 0, -1): # decrement i
    if keep[i, k] == 1: # i.e. we want to keep this as a solution
      solution.append(i-1) # append song i to solution set
      k = k - lengths[i-1] # decrement k by the length of the song

  return solution

args = sys.argv
if len(args) != 2: # need two args
  print str(len(args)) + " is too few args!"
  sys.exit()

C = int(args[1]) # Time interval (in seconds)

songs = ["Something", "something else", "etc"] # example songs list
l = [20, 10, 50] # some song lengths (in seconds)
n = len(songs)

result = []
if sum(l) <= C: # If all the songs will fit in the interval
  result = songs # Best-case: O(n)
else:
  # Worst- and average-case: O(n*C + n) = O(C(1+n)) = O(nC)
  solution = knapsack(l, l, n, C) # Returns indices

  for index in solution:
    result.append(songs[index])

print result

