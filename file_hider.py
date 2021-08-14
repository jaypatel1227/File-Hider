# the goal of this program is to take a few files and hide them in a complicated nested file directory structure

import os
import shutil
import random
import math
from itertools import chain
from english_words import english_words_set
from pathlib import Path

words = iter(english_words_set)

# directory with files you want to hide followed with a /
DIR_NAME = "Files/"

# we will assume that you are running this script from the same directory which where we have the (to be hidden) files
PATH = os.getcwd() + '/'
DIR_PATH = PATH + DIR_NAME
def get_name():
    return next(words)

# count the number of files to be hidden
def count_num_files():
    count = 0
    for _ in os.listdir(DIR_PATH):
        count += 1
    return count

# finds the smallest n such that 2^n > num
def round_2(num):
    # first check if num is a power of 2
    if 2**int(math.log(num, 2)+.5) == num:
        return int(math.log(num, 2)+.5)+1
    return math.ceil(math.log(num,2))

class TreeNode:
    def __init__(self, val, parent = None):
        self.val = val
        self.parent = parent
    def path(self):
        res = ''
        curr = self
        while curr is not None:
            res = str(curr.val) + '/' + res
            curr = curr.parent
        return PATH + res
    def path_obj(self):
        return Path(self.path())
    def __repr__(self):
        return self.path()

def doubling_dirs(base_nodes):
    new_nodes = []
    for node in base_nodes:
        new_nodes.append(TreeNode(get_name(), node))
        new_nodes.append(TreeNode(get_name(), node))
    return new_nodes

def make_subdir_nodes(num):
    res = [TreeNode(get_name())]
    curr = res
    for _ in range(round_2(num)):
        curr = doubling_dirs(curr)
        res = chain(res,curr) # using chain to prevent memory issues for tiny macines or many, many files
    return list(res)

def create_subdirs(nodes):
    for node in nodes:
        node.path_obj().mkdir(parents=True, exist_ok=True)
        
def move_files():
    num = count_num_files()
    nodes = make_subdir_nodes(round_2(num))
    create_subdirs(nodes)
    to_hide = os.listdir(DIR_PATH)
    print(nodes)
    print(to_hide)
    locs = zip(to_hide, random.sample(nodes,num))
    
    for a,b in locs:
        shutil.move(DIR_PATH + a, b.path() + a)

if __name__ == '__main__':
    move_files()