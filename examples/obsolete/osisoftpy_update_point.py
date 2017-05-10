# -*- coding: utf-8 -*-

import collections
import itertools

li = ["username", "password", 'basic', '']

foo = [i for i in itertools.permutations(li, 3)]

# print(*foo, sep='\n')

usernames = frozenset(['albertxu', 'hakaslak', ' ', 'apong'])
passwords = frozenset(['Welcome2pi', 'p@ssw0rd', ''])
authtype = frozenset(['kerberos', 'basic', ''])

fizz = itertools.combinations((usernames, passwords), 1)  # --> AB AC AD BC
# BD CD
buzz = itertools.combinations(range(4), 3)  # --> 012 013 023 123

coke = list(itertools.product(usernames, passwords, authtype))

# print(*fizz, sep='\n')
# print(*buzz, sep='\n')
print(*coke, sep='\n')


def all_subsets(ss):
    return itertools.chain(
        *map(lambda x: itertools.combinations(ss, x), range(0, len(ss) + 1)))


# for subset in all_subsets(usernames):
#     print(subset)
