import re

import lib.aoc
import lib.graph

def parse_bags(s):
    graph = {}
    for line in s.splitlines():
        outer, inner = line.split('bags contain')
        outer = outer.strip()
        contents = []
        for amount, item in re.findall('(\d+) ([\w ]+) bag', inner):
            contents.append((item, int(amount)))
        graph[outer] = contents
    return graph

def can_contain(graph, key, inner):
    for item, amount in graph.get(key, []):
        if item == inner or can_contain(graph, item, inner):
            return True
    return False

def part1(s):
    graph = parse_bags(s)
    answer = sum(1
                 for key
                 in graph.keys()
                 if can_contain(graph, key, 'shiny gold'))
    lib.aoc.give_answer(2020, 7, 1, answer)

def count_contents(graph, bag):
    return sum(n * (1 + count_contents(graph, t))
               for t,n
               in graph[bag])

def part2(s):
    graph = parse_bags(s)
    answer = count_contents(graph, 'shiny gold')
    lib.aoc.give_answer(2020, 7, 2, answer)

INPUT = lib.aoc.get_input(2020, 7)

part1(INPUT)
part2(INPUT)

def leaf_to_root_bags(bag_graph):
    graph = {}
    for key, items in bag_graph.items():
        graph[key] = [t for t,_ in items]
    return lib.graph.topological_sort(graph)

def part1_optimized(s):
    graph = parse_bags(s)
    contains_target = set()
    for bag in leaf_to_root_bags(graph):
        if any(child == 'shiny gold' or child in contains_target
               for child,_
               in graph.get(bag, [])):
            contains_target.add(bag)
    answer = len(contains_target)
    lib.aoc.give_answer(2020, 7, 1, answer)

def part2_optimized(s):
    graph = parse_bags(s)
    bag_content_counts = {}
    for bag in leaf_to_root_bags(graph):
        total = sum(n * (1 + bag_content_counts.get(t, 0))
                    for t,n
                    in graph.get(bag, []))
        bag_content_counts[bag] = total
    answer = bag_content_counts['shiny gold']
    lib.aoc.give_answer(2020, 7, 2, answer)

# This input *WILL* break naive solutions. The optimized solution runs blazing fast though!
INTENSE_INPUT = '''a a bags contain no other bags.
b b bags contain 1 a a bag.
c c bags contain 1 a a bag, 1 b b bag.
d d bags contain 1 a a bag, 1 b b bag, 1 c c bag.
e e bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag.
f f bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag.
g g bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag.
h h bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag.
i i bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag.
j j bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag.
k k bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag.
l l bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag.
m m bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag.
n n bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag.
o o bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag.
p p bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag.
q q bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag.
r r bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag, 1 q q bag.
s s bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag, 1 q q bag, 1 r r bag.
t t bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag, 1 q q bag, 1 r r bag, 1 s s bag.
u u bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag, 1 q q bag, 1 r r bag, 1 s s bag, 1 t t bag.
v v bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag, 1 q q bag, 1 r r bag, 1 s s bag, 1 t t bag, 1 u u bag.
w w bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag, 1 q q bag, 1 r r bag, 1 s s bag, 1 t t bag, 1 u u bag, 1 v v bag.
x x bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag, 1 q q bag, 1 r r bag, 1 s s bag, 1 t t bag, 1 u u bag, 1 v v bag, 1 w w bag.
y y bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag, 1 q q bag, 1 r r bag, 1 s s bag, 1 t t bag, 1 u u bag, 1 v v bag, 1 w w bag, 1 x x bag.
z z bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag, 1 q q bag, 1 r r bag, 1 s s bag, 1 t t bag, 1 u u bag, 1 v v bag, 1 w w bag, 1 x x bag, 1 y y bag.
shiny gold bags contain 1 a a bag, 1 b b bag, 1 c c bag, 1 d d bag, 1 e e bag, 1 f f bag, 1 g g bag, 1 h h bag, 1 i i bag, 1 j j bag, 1 k k bag, 1 l l bag, 1 m m bag, 1 n n bag, 1 o o bag, 1 p p bag, 1 q q bag, 1 r r bag, 1 s s bag, 1 t t bag, 1 u u bag, 1 v v bag, 1 w w bag, 1 x x bag, 1 y y bag, 1 z z bag.
asdf jkl bags contain 1 shiny gold bag.
jkl asdf bags contain 4 zz bags, 1 asdf jkl bag.
totally empty bags contain 42 z z bags.
the answer bags contain 4 shiny gold bags.'''
