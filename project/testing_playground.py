print('This is a testing playground')

test_set = {'apple', 'orange', 'lemon'}
print(test_set)

test_set.add('cherry')
print(test_set)

test_set.add('apple')
print(test_set)

test_dict = {
    'linux' : 'repo',
    'ruby' : 'repo',
    'fozail' : 'user'
}
print(test_dict)

test_dict['sun'] = 'user'
print(test_dict)

test_dict['fozail'] = 'repo'
print(test_dict)

for key,value in test_dict.items():
    print('Key:', key, 'Value:', value)