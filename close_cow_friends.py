# def distance(x):
# 	return pow(pow(x[0], 2)+pow(x[1], 2), 0.5)
#
# def merge_sort(li):
# 	if len(li) < 2: return li
# 	m = len(li) // 2
# 	return merge(merge_sort(li[:m]), merge_sort(li[m:]))
#
#
# def merge(l, r):
# 	global count
# 	result = []
# 	i = j = 0
# 	while i < len(l) and j < len(r):
# 		if l[i] <= r[j]:
# 			result.append(l[i])
# 			i += 1
# 		else:
# 			result.append(r[j])
# 			count = count + (len(l) - i)
# 			j += 1
# 	result.extend(l[i:])
# 	result.extend(r[j:])
# 	return result
#
#
# def change_value(A, i, v):
# 	A[i] = v
# 	while i >= 0:
# 		parent = (i-1)//2
# 		if parent < 0:
# 			parent = 0
# 		if distance(A[i]) < distance(A[parent]):
# 			A[i], A[parent] = A[parent], A[i]
# 			i = parent
# 		else:
# 			sl, sr = 2*i + 1, 2*i + 2
# 			if sr <= len(A):
# 				if distance(A[sl]) < distance(A[i]) or distance(A[sr]) < distance(A[i]):
# 					A[sl], A[i] = A[i], A[sl]
# 					i = sl
# 			elif sl == len(A):
# 				if distance(A[sl]) < distance(A[i]):
# 					A[sl], A[i] = A[i], A[sl]
# 					i = sl
# 			else:
# 				break
# 	return A
#
# def close_cow_friends(locations, g):
# 	"""
# 	Return g locations closest to origin in increasing order.
# 	Input:  locations | generator of location tuples (x, y)
# 			g         | number locations to return
# 	"""
# 	guests = locations[:g]
# 	sorted(guests, key=distance)
# 	for i in range(g, len(locations)):
# 		change_value(guests, g-1, locations)
# 	return guests
# count = 0
#
#
# def distance(x):
# 	a, b = x
# 	return pow(pow(a, 2) + pow(b, 2), 0.5)
#
#
# def merge_sort(li):
# 	if len(li) < 2: return li
# 	m = len(li) // 2
# 	return merge(merge_sort(li[:m]), merge_sort(li[m:]))
#
#
# def merge(l, r):
# 	global count
# 	result = []
# 	i = j = 0
# 	while i < len(l) and j < len(r):
# 		if distance(l[i]) <= distance(r[j]):
# 			result.append(l[i])
# 			i += 1
# 		else:
# 			result.append(r[j])
# 			count = count + (len(l) - i)
# 			j += 1
# 	result.extend(l[i:])
# 	result.extend(r[j:])
# 	return result
#
#
# def change_value(A, i, v):
# 	A[i] = v
# 	while i >= 0:
# 		parent = (i-1)//2
# 		if parent < 0:
# 			parent = 0
# 		if distance(A[i]) < distance(A[parent]):
# 			A[i], A[parent] = A[parent], A[i]
# 			i = parent
# 		elif i > 0 and i%2 == 0 and distance(A[i-1]) > distance(A[i]):
# 			A[i-1], A[i] = A[i], A[i-1]
# 			i = i-1
# 		elif i > 0 and (i+1)%2 == 0 and distance(A[i]) > distance(A[i+1]):
# 			A[i+1], A[i] = A[i], A[i+1]
# 			i = i+1
# 		else:
# 			sl, sr = 2*i + 1, 2*i + 2
# 			# print(len(A),sl,i)
# 			if sl <= len(A)-1:
# 				if distance(A[sl]) < distance(A[i]):
# 					A[sl], A[i] = A[i], A[sl]
# 					i = sl
# 			else:
# 				break
# 	return A
#
#
# def close_cow_friends(locations, g):
# 	"""
# 	Return g locations closest to origin in increasing order.
# 	Input:  locations | generator of location tuples (x, y)
# 			g         | number locations to return
# 	"""
# 	guests, rest = [], []
# 	j = 0
# 	for i in locations:
# 		if j < g:
# 			guests.append(i)
# 			j += 1
# 		else:
# 			rest.append(i)
# 			j += 1
# 	# print(guests)
# 	guests = merge_sort(guests)
# 	# print(guests)
# 	for i in rest:
# 		if distance(guests[g - 1]) > distance(i):
# 			change_value(guests, g - 1, i)
# 	return guests
def distance(x):
	a, b = x
	a = int(100 * a)
	b = int(100 * b)
	return a*a + b*b


def merge_sort(li):
	if len(li) < 2: return li
	m = len(li) // 2
	return merge(merge_sort(li[:m]), merge_sort(li[m:]))


def merge(l, r):
	result = []
	i = j = 0
	while i < len(l) and j < len(r):
		if distance(l[i]) <= distance(r[j]):
			result.append(l[i])
			i += 1
		else:
			result.append(r[j])
			j += 1
	result.extend(l[i:])
	result.extend(r[j:])
	return result


def change_value(A, i, v):
	A[i] = v
	while i >= 0:
		parent = (i - 1) // 2
		if parent < 0:
			parent = 0
		if distance(A[i]) < distance(A[parent]):
			A[i], A[parent] = A[parent], A[i]
			i = parent
		elif i > 0 and i % 2 == 0 and distance(A[i - 1]) > distance(A[i]):
			A[i - 1], A[i] = A[i], A[i - 1]
			i = i - 1
		elif len(A) - 2 >= i > 0 == (i + 1) % 2 and distance(A[i]) > distance(A[i + 1]):
			A[i + 1], A[i] = A[i], A[i + 1]
			i = i + 1
		else:
			sl, sr = 2 * i + 1, 2 * i + 2
			if sl <= len(A) - 1:
				if distance(A[sl]) < distance(A[i]):
					A[sl], A[i] = A[i], A[sl]
					i = sl
			else:
				break


def close_cow_friends(locations, g):
	"""
	Return g locations closest to origin in increasing order.
	Input:  locations | generator of location tuples (x, y)
			g         | number locations to return
	"""
	guests, rest = [], []
	j = 0
	for i in locations:
		if j < g:
			guests.append(i)
			j += 1
		else:
			rest.append(i)
			j += 1
	guests = merge_sort(guests)
	for i in rest:
		if distance(guests[g - 1]) > distance(i):
			print(i)
			change_value(guests, g - 1, i)
	return guests

g = 5
a = [(-3.085938209482254, -35.51086598631448), (26.993450139920384, 0.8331111535179057), (18.498724377558744, 30.754288731062978), (6.608602405714086, 29.946996046275647), (-6.474375132714367, 11.891001424902061), (2.6030415461917915, -23.33983716414429), (20.043810572570063, -34.85060665721733), (23.528508854561295, -2.4642560026968043), (-38.75851406006202, 14.135701382849792), (-25.728316581837667, -26.455843842973806)]
ans = close_cow_friends(a, g)

# Our solution produced the following value for ans:
tf = (ans == [(-6.474375132714367, 11.891001424902061), (2.6030415461917915, -23.33983716414429), (23.528508854561295, -2.4642560026968043), (26.993450139920384, 0.8331111535179057), (6.608602405714086, 29.946996046275647)])