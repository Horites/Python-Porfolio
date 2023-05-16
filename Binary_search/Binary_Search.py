def binary_search(arr, x, low = 0, high = None):

    # Initialize "high" if not known.
    if high is None:
        high = len(arr)

    # Base case - we didn't find it.
    if low >= high:
        print(f"Can't find {x} in {arr}")
        return -1
    
    # Look for it in the middle.
    m = (low + high) // 2
    if arr[m] == x:
        print(f"Found {x} at index {m}!")
        return x
    
    # Otherwise divide and conquer.
    elif arr[m] > x:
        # Search lower half.
        binary_search(arr, x, low, m)
    else:
        binary_search(arr, x, m + 1, high)

# Test
binary_search([1, 4, 7, 20, 99], 7)
binary_search([3, 8, 2, 23, 35, 48, 98], 48)
binary_search([3, 4, 5, 6, 7], 7)
binary_search([1, 2, 3], 4)
binary_search([0, 99], 99)