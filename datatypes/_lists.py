
import redis

mylist = list()

# Lists
# lpush & rpush
# lpushx & rpushx
# lpop & rpop
# lindex 
# llen 
# lrem
# lset
# lrange
# delete

with redis.Redis(host='127.0.0.1', port=6379) as client:
    client.flushall()

    client.lpush('mylist', 'first_member')
    mylist.insert(0, 'first_member')

    client.rpush('mylist', 'last_member')
    mylist.append('last_member')

    # Those will not be added because such list does not exist, values will be added to list, if such list with given name exists
    client.lpushx('non_existing_list', 'first_member ++')
    client.rpushx('non_existing_list', 'last_member ++')

    redis_list = client.lrange('mylist', 0, -1)  # show all elements
    # [b'first_member', b'last_member'] <class 'list'> ~ list of bytes objects
    print(redis_list, type(redis_list))
    # ['first_member', 'last_member']
    print(mylist)

    nums = list()
    for i in range(1, 101):
        client.rpush('nums', i)
        nums.append(i)

    first_50 = client.lrange('nums', 0, 49)
    print(first_50, len(first_50))
    # [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'10', b'11', b'12', b'13', b'14', b'15', b'16', b'17', b'18', b'19', b'20', b'21', b'22', b'23', b'24', b'25', b'26', b'27', b'28', b'29', b'30', b'31', b'32', b'33', b'34', b'35', b'36', b'37', b'38', b'39', b'40', b'41', b'42', b'43', b'44', b'45', b'46', b'47', b'48', b'49', b'50']
    # 50 - length

    # Delete and return value
    last_num = int(client.rpop('nums').decode())
    first_num = int(client.lpop('nums').decode())

    _last_num = nums.pop()
    _first_num = nums.pop(0)

    print(last_num == _last_num)      # True 100 == 100
    print(first_num == _first_num)    # True   1 == 1

    # Delete without returning
    # Remove the first count (1) occurrences of elements equal to value (first_member) from the list stored at name (mylist)
    client.lrem('mylist', count=1, value='first_member')

    # Get the lenght of the list (returns integer)
    print(client.llen('nums'), len(nums))  # 98 98

    client.lset('nums', -2, 'penultimate')
    nums.insert(-1, 'penultimate')

    penultimate_val = client.lindex('nums', -2).decode()
    print(penultimate_val, nums[-2])    # penultimate penultimate

    del mylist
    client.delete('mylist')
