import redis

# To make sure you understand everything corresponding commands in redis for lists will be shown with python sets' commands:
myset = set()


# Redis sets are an unordered collection of strings
# In this tutorial we are gonna cover following commands for sets:
# sadd
# smembers
# sismember
# scard
# sunion
# sinter
# sdiff
# srem
# spop
# srandmember

with redis.Redis(host='127.0.0.1', port=6379) as client:
    # Add values to a set:
    client.sadd('myset', 5)
    client.sadd('myset', 'Hi', 5)
    myset.add(5)
    myset.add('Hi')
    myset.add(5)

    # Get all elements of a set:
    elements = client.smembers('myset')
    print(myset, elements)  # {5, 'Hi'} {b'5', b'Hi'}

    # Get the lenght (cardinality) of a set:
    length = client.scard('myset')
    print(len(myset), length)  # 2 2

    client.sadd('her_set', 'jika', 25)
    client.sadd('his_set', 'pika', 'jika', 5)

    her_set = {'jika', 25}
    his_set = {'pika', 'jika', 5}

    # Get union of given sets:
    union = client.sunion('myset', 'her_set', 'his_set')
    py_union = myset.union(his_set, her_set)

    print(py_union, union) # {5, 'pika', 'jika', 'Hi', 25} {b'pika', b'jika', b'Hi', b'5', b'25'}

    # Get elements that are present in all given sets (intersection):
    intersection = client.sinter('myset', 'his_set')
    py_intresection = myset.intersection(his_set)

    print(py_intresection, intersection)  # {5} {b'5'}

    # Get elements that are unique for given set among other given sets:
    difference = client.sdiff('myset', 'her_set', 'his_set')
    py_difference = myset.difference(her_set, his_set)

    print(py_difference, difference) # {'Hi'} {b'Hi'} ~ means 'Hi' does not exist in her_set and his_set it is only pertains to myset

    # Check if element exists in a set:
    if client.sismember('myset', 'jika'):
        print('jika exists in myset')
    else:
        print('jika does not exist in myset')
      # Output: jika does not exist in myset

    # Move elements from one set to another:
    client.smove('his_set', 'her_set', 'pika')                      # .smove(from_set, destination_set, value)
    print(client.smembers('his_set'), client.smembers('her_set'))   # {b'5', b'jika'} {b'25', b'pika', b'jika'}
    # 'pika' is now pertains to her_set
    # python sets do not have such command, so:
    his_set.remove('pika')
    her_set.add('pika')
    print(his_set, her_set)  # {'jika', 5} {'jika', 'pika', 25}

    # Remove elements from a set:
    client.sadd('nums', *(i for i in range(100)))
    nums = {i for i in range(100)}
    client.srem('nums', 45, 90)
    random_element = client.spop('nums') # count stands for amount of random elements to delete (by default None): client.spop('nums', count=20) - returns and deletes 20 random elements

    nums.remove(45)
    nums.remove(90)
    py_random_element = nums.pop()  # removes and returns first element

    print(py_random_element, random_element)  # 0 b'79'

    # Only get random element:
    random_element = client.srandmember('nums') # to get multiple random elements specify the value for 'number'
    print(random_element) # b'46'

    client.flushall()
