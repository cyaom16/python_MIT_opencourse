# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    result = [sequence]
    def insert(pivot, lst):
        if not isinstance(lst, list):
            lst = [lst]
        result = []
        for word in lst:
            result.extend([word[i:] + pivot + word[:i] for i in xrange(len(word), -1, -1)])

        return result


    if len(sequence) == 1:
        return result
    else:
        result.extend(insert(sequence[0], get_permutations(sequence[1:])))

    return list(set(result))

if __name__ == '__main__':

   test_input = 'abc'
   print('Input 1:', test_input)
   print('Expected Output 1:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
   print('Actual Output 1:', get_permutations(test_input))

   test_input2 = 'ab'
   print('Input 2:', test_input2)
   print('Expected Output 2:', ['ab', 'ba'])
   print('Actual Output 2:', get_permutations(test_input2))

   test_input3 = 'yzx'
   print('Input 3:', test_input3)
   print('Expected Output 3:', ['yzx', 'yxz', 'zxy', 'zyx', 'xyz', 'xzy'])
   print('Actual Output 3:', get_permutations(test_input3))