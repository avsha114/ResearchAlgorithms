import sys
import math

# My variables:
total_earnings = 0
groups = []
earning_cache = dict()
index_cache = dict()
index = 0

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l, c, n = [int(i) for i in input().split()]
for i in range(n):
    pi = int(input())
    # My addition:
    groups.append(pi)

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

for i in range(c):
    seats_taken = 0
    start_index = index
    skip = False

    while seats_taken <= l:
        # If already calculated:
        if start_index in earning_cache:
            total_earnings += earning_cache[start_index]
            index = index_cache[start_index]
            break

        # If index hasn't changed after 1 iteration we should skip:
        if start_index == index:
            if skip: break
            skip = True

        # Mark seats and move index to the next group:
        if seats_taken + groups[index] <= l:
            seats_taken += groups[index]
            index = index+1 if index+1 < len(groups) else 0
        else:
            break

    total_earnings += seats_taken

    # Add earnings to cache for future use:
    if not start_index in earning_cache:
        earning_cache[start_index] = seats_taken
        index_cache[start_index] = index

print(total_earnings)
