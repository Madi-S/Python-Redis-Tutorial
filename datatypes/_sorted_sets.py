import redis

# Unfortunately, python does not have such datatype,, so we are unable to compare similar commands.
# Redis sorted sets are collection of non-repeating strings, where each string is acossiated with a score that is used to order sortes sets and indicates member's rank (index).
# In this tutorial we are gonna cover following commands for sorted sets:

with redis.Redis(host='localhost', port=6379) as client:
    client.flushall()
    if client.ping():  # Ping the redis server (returns True or False)
        print('Pong')

    # To add values to a sortes set:
    client.zadd('records', {'player_1': 1059,
                            'player_2': 871,
                            'player_3': 1298,
                            'player_4': 591,
                            'player_5': 981,
                            'player_6': 1301,
                            })

    """
    zadd other arguments:
    
    nx - only create new elements and not to update scores for elements that already exist.

    xx - only update scores of elements that already exist. New elements will not be added.

    ch - modifies the return value to be the numbers of elements changed. Changed elements include new elements that were added and elements whose scores changed.

    incr - modifies ZADD to behave like ZINCRBY. In this mode only a single element/score pair can be specified and the score is the amount the existing score will be incremented by. When using this mode the return value of ZADD will be the new score of the element.

    The return value of ZADD varies based on the mode specified. With no options, ZADD returns the number of new elements added to the sorted set.
    """

    # Get the lenght (cardinality):
    length = client.zcard('records')
    print(length)  # 6

    # Get elements:
    # Return elements that have scores between 0 and 1000 
    print(client.zrangebyscore('records', 0, 1000, withscores=True))  # [(b'player_4', 591.0), (b'player_2', 871.0), (b'player_5', 981.0)]
    # Return elements from second to fifth positions, which are sorted by score (desc stands for descending order)
    print(client.zrange('records', 2, 5, withscores=True, desc=True)) # [(b'player_1', 1059.0), (b'player_5', 981.0), (b'player_2', 871.0), (b'player_4', 591.0)]

    # Get the number of elements between given min and max scores:
    number = client.zcount('records', 1000, 1500)
    print(number)  # 3

    # Increment the score of member:
    incremented = client.zincrby('records', 5000, 'player_6') # # 1301 + 5000 (the amount can negative, float too)
    print(incremented)  # 6301.0

    # Get rank(index) of an element:
    index = client.zrank('records', 'player_1')
    rev_index = client.zrevrank('records', 'player_1')
    print(index, rev_index)  # 3 2

    # Get score of member:
    score = client.zscore('records', 'player_2')
    print(score) # 871.0

    # Delete and return max and min elements:
    max_ = client.zpopmax('records')
    # Delete two elements with consecutive lowest scores
    mins = client.zpopmin('records', count=2)

    # Delete and not return elements:
    client.zadd('to_del', {i: i*i for i in range(100)})
    print(client.zrange('to_del', 45, 47, withscores=True)) # [(b'45', 2025.0), (b'46', 2116.0), (b'47', 2209.0)]

    removed_count = client.zrem('to_del', 30, 31, 32)
    print(removed_count)                        # 3
    print(client.zrange('to_del', 30, 32))      # [b'33', b'34', b'35']

    client.zremrangebyrank('records', 0, -1)
    print(client.zrange('records', 0, -1))      # []

    removed_count = client.zremrangebyscore('to_del', 1000, 5000)
    print(client.zcount('to_del', 1000, 5000))  # 0

    client.flushall()
