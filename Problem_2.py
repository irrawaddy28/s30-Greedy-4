'''
1007 Minimum Domino Rotations For Equal Row
https://leetcode.com/problems/minimum-domino-rotations-for-equal-row/description/

In a row of dominoes, tops[i] and bottoms[i] represent the top and bottom halves of the ith domino. (A domino is a tile with two numbers from 1 to 6 - one on each half of the tile.)

We may rotate the ith domino, so that tops[i] and bottoms[i] swap values.

Return the minimum number of rotations so that all the values in tops are the same, or all the values in bottoms are the same.

If it cannot be done, return -1.

Example 1:
Input: tops = [2,1,2,4,2,2], bottoms = [5,2,6,2,3,2]
Output: 2
Explanation:
The first figure represents the dominoes as given by tops and bottoms: before we do any rotations.
If we rotate the second and fourth dominoes, we can make every value in the top row equal to 2, as indicated by the second figure.

Example 2:
Input: tops = [3,5,1,2,3], bottoms = [3,6,3,3,4]
Output: -1
Explanation:
In this case, it is not possible to rotate the dominoes to make one row of values equal.

Constraints:
2 <= tops.length <= 2 * 10^4
bottoms.length == tops.length
1 <= tops[i], bottoms[i] <= 6

Solution
1. Greedy
First, we choose tops[0] as the target

Read tops and bottoms array one index at a time and test the following conditions:

If the target is not present in both the tops[index] and bottoms[index], then it is impossible to have this target across all of tops[] or bottoms[]. Return inf.

If the target is present in tops[index] but not bottoms[index], then move target from tops to bottoms. Increment t2b_rots by 1.

If the target is not present in tops[index] but in bottoms[index], then move target from bottoms to tops. Increment b2t_rots by 1.

If the target is present in both the tops[index] and bottoms[index], then nothing to be incremented.

We find x = min(t2b_rots, b2t_rots)

Now, we choose bottoms[0] as the target and repeat the steps again.
We find y = min(t2b_rots, b2t_rots)

We finally return min(x, y)

https://youtu.be/ghAK4ONksDo?t=3461

Time: O(N), Space: O(1)
'''
from typing import List

def minDominoRotations(tops: List[int], bottoms: List[int]) -> int:
    if not tops or not bottoms:
        return -1

    N = len(tops)
    assert N == len(bottoms), \
           f"len(tops) ({N}) != len(bottoms) ({len(bottoms)})"

    result = [N+1, N+1]
    for ind, target in enumerate([tops[0], bottoms[0]]):
        t2b_rots = b2t_rots = 0
        for i in range(N):
            if tops[i] != target and bottoms[i] != target:
                # target doesn't exist in both tops and bottoms
                t2b_rots = b2t_rots = N+1
                break
            elif tops[i] != target: # bottoms[i] == target is guaranteed
                # target in bottoms array, move from bottoms to tops
                b2t_rots += 1
            elif bottoms[i] != target: # tops[i] == target is guaranteed
                # target in tops array, move from tops to bottoms
                t2b_rots += 1
        result[ind] = min(t2b_rots, b2t_rots)

    if min(result) == N+1:
        return -1
    return min(result)

def run_minDominoRotations():
    tests = [([2,1,2,4,2,2], [5,2,6,2,3,2], 2), # move 2, cannot move 5
             ([5,2,5,2,5,2], [2,5,2,5,2,5], 3), # move either 2 or 5
             ([5,2,5,2,5,5], [2,5,2,5,2,5], 2), # move 5, cannot move 2
             ]
    for test in tests:
        tops, bottoms, ans = test[0], test[1], test[2]
        print(f"\ntops: {tops}")
        print(f"bottoms: {bottoms}")
        min_rots = minDominoRotations(tops, bottoms)
        success = (ans == min_rots)
        print(f"Pass: {success}")
        if not success:
            print(f"Failed")
            return

run_minDominoRotations()
