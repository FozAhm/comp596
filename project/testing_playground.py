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

tuple1 = ('loysoft/node-oauth2-server', 'adieuadieu/node-oauth2-server')
tuple2 = ('django/django', 'm1guelpf/django')

test_dict[tuple1] = 1
test_dict[tuple2] = 2

for key,value in test_dict.items():
    print('Key:', key, 'Value:', value)

test_dict[tuple2] = test_dict[tuple2] + 1

for key,value in test_dict.items():
    print('Key:', key, 'Value:', value)