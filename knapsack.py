import queue
from collections import namedtuple
import pandas as pd
#this is for accessing github data
file_location = 'https://raw.githubusercontent.com/Tanvir19934/0-1-Knapsack-Problem/main/data/ks_50_0'
input_data = pd.read_csv(file_location, header = None)
import numpy as np
from collections import defaultdict

Item = namedtuple("Item", ['index', 'value', 'weight'])
# parse the input
input_data = input_data.iloc[:,0].str.split(' ')
lines = list(input_data)
lines = np.array(lines,dtype=int)
item_count = int(input_data[0][0])
capacity = int(input_data[0][1])

items = []

for i in range(1, item_count+1):
    line = lines[i]
    parts = line
    items.append(Item(i-1, int(parts[0]), int(parts[1])))

items_sorted = sorted(items, key=lambda k: float(k.value)/k.weight, reverse = True)

################## Branch and Bound- Breadth First Search (BFS) ######################


class Node:
    def __init__(self, level, value, weight, bound, contains):
         self.level = level
         self.value = value
         self.weight = weight
         self.bound = bound
         self.contains = contains

def upper_bound(u, k, n, v, w):
        if u.weight > k:
            return 0
        else:
            bound = u.value
            wt = u.weight
            j = u.level 
            while j < n and wt + w[j] <= k:
                bound += v[j]
                wt += w[j]
                j += 1
            # fill knapsack with fraction of a remaining item
            if j < n:
                bound += (k - wt) * float(v[j]/ w[j])
                #bound += v[j]
            return bound


def knapsack(items, capacity):
        item_count = len(items)
        v = [0]*item_count
        w = [0]*item_count

        # sort items by value to weight ratio
        items = sorted(items, key=lambda k: float(k.value)/k.weight, reverse = True)
        for i,item in enumerate(items, 0):
            v[i] = int(item.value)
            w[i] = int(item.weight)
        #creating a queue. BFS algorithm is implemented via a queue (FIFO method)
        q = queue.Queue()
        root = Node(0, 0, 0, 0.0,[])
        root.bound = upper_bound(root, capacity, item_count, v, w)
        q.put(root)
        value = 0
        taken_sorted = [0]*item_count
        best = []
        while not q.empty():
            c = q.get()
            if c.bound > value:
                level = c.level+1
            # check 'left' node (if item is added to knapsack)
            left = Node(level,c.value + v[level-1], c.weight + w[level-1], 0.0, c.contains[:])
            left.bound = upper_bound(left, capacity, item_count, v, w)
            left.contains.append(level)
            if left.weight <= capacity:
                if left.value > value:
                    value = left.value
                    best = left.contains
                if left.bound > value:
                    q.put(left)
                # check 'right' node (if items is not added to knapsack)   
            right = Node(level,c.value, c.weight, 0.0, c.contains[:])
            right.bound = upper_bound(right, capacity, item_count, v, w)
            if right.weight <= capacity:
                if right.value > value:
                    value = right.value
                    #best = set(right.contains)
                if right.bound > value:
                    q.put(right)
        for b in best:
            taken_sorted[b-1] = 1

        #turning taken indices which is in terms of sorted items to
        #taken which is in terms of the original items namedtuple    
        taken_indices = []
        for i in range(0,item_count):
          if taken_sorted[i]==1:
            taken_indices.append(items_sorted[i].index)
        taken = [0]*item_count
        for i in range(0,len(taken_indices)):
          taken[taken_indices[i-1]] = 1
        
        return taken

taken = knapsack(items, capacity)

#getting value and weight in terms of the original items namedtuple
v = [0]*item_count
w = [0]*item_count
for i,item in enumerate(items, 0):
            v[i] = int(item.value)
            w[i] = int(item.weight)
total_weight = sum([i*j for (i,j) in zip(w,taken)])
total_value = sum([i*j for (i,j) in zip(v,taken)])

#producing output data
output_data = str(total_value) + ' ' + str(0) + '\n'
output_data += ' '.join(map(str, taken))
print(output_data)

