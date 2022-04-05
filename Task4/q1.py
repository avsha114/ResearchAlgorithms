# This is a generator for all subsets of 's' that their sum are 'c' or less
def bounded_subsets(s : set, c : int):
    # We sort the elements first to avoid checking irrelevant subsets
    elements = sorted(s)
    s_size = len(elements)

    # get_perm is a function that creates a string that represents a subset
    # We represent numbers as binary form string and check that subset
    # If the char in index i equals 0 -> the element in index i is NOT in the subset
    # If the char in index i equals 1 -> the element in index i is in the subset
    # Finally, we reverse the string to start with the smallest number
    # For example for 3 elements the string will be: 000, 100, 010......
    get_perm = lambda x: format(x, 'b').zfill(s_size)[::-1]
    perm_number = 1

    # First return empty set
    yield []

    # If we have more than 0 elements:
    while s_size > 0:
        # Get the current binary string form of the subset
        current_perm = get_perm(perm_number)

        # If the smallest number in this permutation > c
        # than we can break the while loop and end the generator
        smallest_element_index = current_perm.find("1")
        if elements[smallest_element_index] > c:
            break

        # Now we compute the sum of the current subset
        temp_sum = 0
        temp_set = []
        is_valid_subset = True # Flag when to stop adding elements
        for i in range(s_size):
            if current_perm[i] != '0':
                # If the sum > c than we can stop iterating and continue to the next permutation
                if temp_sum + elements[i] > c:
                    is_valid_subset = False
                    break
                temp_sum += elements[i]
                temp_set.append(elements[i])

        # Yield return the current subset
        if is_valid_subset:
            yield temp_set

        # if the next binary number string size is larger than the elements count,
        # We can end the generator
        perm_number += 1
        if len((format(perm_number, 'b'))) > s_size:
            break

if __name__ == '__main__':
    print("####################")
    print("Test1:")
    # Result: [] [1] [2] [1, 2] [3]
    for e in bounded_subsets([1, 2, 3], 3):
        print(e)

    print("####################")
    print("Test2:")
    # Result: [] [4] [5] [4, 5] [6] [4, 6] [5, 6] [4, 5, 6]
    for e in bounded_subsets([4, 5, 6], 15):
        print(e)

    print("####################")
    print("Test3:")
    # Result: []
    for e in bounded_subsets([20, 30], 10):
        print(e)

    print("####################")
    print("Test4:")
    # Result: []
    for e in bounded_subsets([], 5):
        print(e)

