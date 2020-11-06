import redis

# Unfortunately, python dictionaries do not have such variety of methods, so we are unable to compare similar commands.
# Redis hashes are basically dictionaries with some more advanced commands
# In this tutorial we are gonna cover following commands for hashes:

# hset (with mapping)
# hget
# hgetall
# hkeys
# hvals
# hlen
# hexists
# hsetnx
# hincrby
# hincrbyfloat
# hmget
# hmset
# hdel


with redis.Redis(host='127.0.0.1', port=6379) as client:
    client.hset('Car', 'Price', '50000$')           # Structure be like client.hset(hash_name, key and value or mapping=dict)
    
    data = {'Price': '15000$'}
    client.hset('Car', mapping=data)                # Single key-value (dict) pair must be passed as an argument 
    
    # Get all keys or/and values and length:
    car_data = client.hgetall('Car')
    keys = client.hkeys('Car')
    values = client.hvals('Car')
    length = client.hlen('Car')
    
    print(car_data, keys, values, length)           # {b'Price': b'50000$'} [b'Price'] [b'50000$'] 1
    print(client.hget('Car', 'Price'))              # b'50000$
    
    # Check if given key exists in a hash:
    if not client.hexists('Car', 'Speed'):
        print('Speed of the car is not given')
        client.hset('Car', 'Speed (km/h)', 270)
    
    # Increment value in a hash:
    client.hincrby('Car', 'Speed (km/h)', 30)
    client.hincrbyfloat('Car', 'Speed (km/h)', -2.5)
    print(client.hget('Car', 'Speed (km/h)'))       # 270 + 30 - 2.5 = 297.5

    # Add key-value pair if hash with given name does not exists:
    client.hsetnx('Person', 'Name', 'John')
    client.hsetnx('Person', 'Name', 'Maximilian')   # Thus this key-value pair will not ovewrite existing key-value pair in Person hash
    print(client.hget('Person', 'Name'))            # b'John'

    person_data = {'Married?': 'Yes',
                   'Homeless?': 'No',
                   'Socially active?': 'No'}
    
    # Set multiple key-value pairs to a hash:
    client.hmset('Person', person_data)             # A dictionary with multiple key-value pairs can be used in hmset as mapping

    # Gett multiple values from a hash:
    print(client.hmget('Person', 'Married?', 'Homeless?'))  # [b'Yes', b'No']

    # Delete key-value pair from a hash:
    client.hdel('Person', 'Name')
    print(client.hget('Person', 'Name'))            # None
    
    # On deleting a stored key, redis returns True if it was deleted successsfully
    if client.delete('Car'):
        print('Hash "Car" was deleted')

    if client.delete('Person'):
        print('Hash "Person" was deleted')
