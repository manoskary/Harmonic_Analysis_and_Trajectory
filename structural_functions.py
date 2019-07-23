
def get_closest_value(arr, target):
    n = len(arr)
    left = 0
    right = n - 1
    mid = 0

    # edge case - last or above all
    if target >= arr[n - 1]:
        return arr[n - 1]
    # edge case - first or below all
    if target <= arr[0]:
        return arr[0]
    # BSearch solution: Time & Space: Log(N)

    while left < right:
        mid = (left + right) // 2  # find the mid
        if target < arr[mid]:
            right = mid
        elif target > arr[mid]:
            left = mid + 1
        else:
            return arr[mid]

    if target < arr[mid]:
        return find_closest(arr[mid - 1], arr[mid], target)
    else:
        return find_closest(arr[mid], arr[mid + 1], target)


def find_closest(val1, val2, target):
    return val2 if target - val1 >= val2 - target else val1


def getKeyByValue(dictOfElements, valueToFind):
    for key, value in dictOfElements.items():
        if value == valueToFind:
            return key


def mergeDicts(dict1, dict2):
    res = {**dict1, **dict2}
    return res
