'''
1055 Shortest Way To Form String
https://leetcode.com/problems/shortest-way-to-form-string/description/

A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (i.e., "ace" is a subsequence of "abcde" while "aec" is not).

Given two strings source and target, return the minimum number of subsequences of source such that their concatenation equals target. If the task is impossible, return -1.


Example 1:
Input: source = "abc", target = "abcbc"
Output: 2
Explanation: The target "abcbc" can be formed by "abc" and "bc", which are subsequences of source "abc".

Example 2:
Input: source = "abc", target = "acdbc"
Output: -1
Explanation: The target string cannot be constructed from the subsequences of source string due to the character "d" in target string.

Example 3:
Input: source = "xyz", target = "xzyxz"
Output: 3
Explanation: The target string can be constructed as follows "xz" + "y" + "xz".


Constraints:
1 <= source.length, target.length <= 1000
source and target consist of lowercase English letters.

1. Hash Set
We add the characters in the source string to a hash set.
We go through the target char-by-char, check if the char is present in the set or not and try matching its characters with the source from start to end. Every time we reach the end of source, we count it as one subsequence. If a character in target isn't in source, we return -1 since it can't be formed.
https://youtu.be/l-66hlFDgZI?t=291 (problem definition, s = xyz, t = xzyxz)
https://youtu.be/l-66hlFDgZI?t=738 (dry run 1)
https://youtu.be/l-66hlFDgZI?t=814 (dry run 2, s = xyz, t = xzyxz)
https://youtu.be/l-66hlFDgZI?t=1471 (dry run 3, TC analysis)

Time: O(MN), Space: O(1), M = len(source), N = len(Target)

2. Hash Map
We add the characters in the source string and the corresponding indices to a hash map (<char, [index]>). To match the character in the target string, we move the source pointer directly to the matching character in the source string
instead of doing linear traversal through the array.

https://youtu.be/l-66hlFDgZI?t=2002 (dry run, s = xyz, t = xzyxz)

Time: O(N log M), Space: O(1), M len(source), N = len(Target)
'''
from collections import defaultdict
def shortestWay_1(source: str, target: str) -> int:
    ''' Using hash set
        Time: O(MN), Space: O(1), M = len(source), N = len(Target)
    '''
    if not target:
        return 0

    M = len(source)
    N = len(target)
    ps, pt = 0, 0 # pointers to 1st char is src and tgt
    result = []
    subseq = ''
    h = set()
    for i in range(M):
        h.add(source[i])
    count = 1

    while pt < N:
        c = target[pt]

        if c not in h:
            return -1, []

        if c == source[ps]:
            # valid case: move both the source and target pointer forward by
            # 1 step
            ps += 1
            pt += 1
            subseq += c
        elif c != source[ps]:
            # invalid case: move only the source pointer forward
            # since target char has not been matched
            ps += 1

        # if we have not reached the end of target string
        # but we have reached the end of source string, then
        # we have constructed another subsequence from the source
        # string. Increment count by 1.
        if pt < N and ps == M:
            count += 1
            ps = 0
            result.append(subseq)
            subseq=''
    if subseq: result.append(subseq)
    return count, result


def shortestWay_2(source: str, target: str) -> int:
    ''' Using hash map
        Time: O(N log M), Space: O(1), M len(source), N = len(Target)
    '''
    def binarySearch(lst, target):
        low, high = 0, len(lst) - 1

        while low <= high:
            mid = low + (high - low) // 2
            if lst[mid] == target:
                return mid
            elif lst[mid] > target:
                high = mid - 1
            else:
                low = mid + 1
        return low

    M = len(source)
    N = len(target)
    ps, pt = 0, 0 # pointers to 1st char is src and tgt
    result = []
    subseq = ''
    h = defaultdict(list)
    # Add <char, index> pairs to the hash map. Note that the source string
    # might have repeating characters in which case we store all the indices
    # of the repeating char in a list
    for i in range(M):
        c = source[i]
        h[c].append(i)
    count = 1

    while pt < N: # O(N)
        c = target[pt]

        if c not in h:
            return -1, []

        # get the list of indices (of the target char c) in source string s
        indices = h[c]
        # Do a binary search (on the indices list)
        # to get the index in s that is just greater than ps
        # Why index just greater than ps? Because to continue expanding
        # the current subsequence, we need to pick a character in the source
        # string that matches the current char in t (i.e., t[pt]) and
        # which also lies after the current pointer (ps) in the source string
        ind = binarySearch(indices, ps) # O (log M)
        if ind == len(indices) or indices[ind] < ps:
            # invalid case:
            # if the index found is out of bounds of the
            # indices array or if the index is less than the current
            # source pointer, set the source pointer to end of string
            # and don't move the target pointer since target char has
            # not been matched
            ps = M
        else:
            # valid case: move both the source and target pointer forward by 1
            # step
            ps = indices[ind]
            ps += 1
            pt += 1
            subseq += c

        if pt < N and ps == M:
            count += 1
            ps = 0
            result.append(subseq)
            subseq=''
    if subseq: result.append(subseq)
    return count, result

def run_shortestWayToFormString():
    tests = [("xyz", "xzyxz", 3), ("abc", "abcbc", 2), ("abc", "acdbc", -1)]
    for test in tests:
        source, target, ans = test[0], test[1], test[2]
        print(f"\nsource string = {source}")
        print(f"target string = {target}")
        for method in [1, 2]:
            if method == 1:
                num_subseqs, result = shortestWay_1(source, target)
            elif method == 2:
                num_subseqs, result = shortestWay_2(source, target)
            print(f"Method {method}: num subsequences = {num_subseqs} ({result})")
            success = (ans == num_subseqs)
            print(f"Pass: {success}")
            if not success:
                print(f"Failed")
                return

run_shortestWayToFormString()
