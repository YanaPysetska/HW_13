# #tst = {
# 	'1': 'a',
# 	'2': 'b',
# 	'3': 'c',
# 	'4': 'd'
# }
# Переберите его циклом и получите следующий список:

[0, 'a', 1, 'b', 2, 'c']
tst = {
	'1': 'a',
	'2': 'b',
	'3': 'c',
	'4': 'd'
}
only_values=[]
for key in tst:
    only_values.append(tst[key])
print(only_values)
new_list=[]
for item in enumerate(only_values):
    key, value = item
    new_list.append((key,value))
    res=new_list[0:3:]
print(res)
new_list = []
for tuple in res:
    new_list.extend(tuple)
print(new_list)





