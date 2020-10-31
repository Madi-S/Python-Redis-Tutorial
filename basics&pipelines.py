import redis
import pickle
import datetime
import time

# To connect to redis server
client = redis.Redis(host='127.0.0.1', port=6379)


# Simple get/set operations for name value pairs:
client.set('name', 'Peter')
name = client.get('name')
print(type(name))               # <class 'bytes'>
print(name.decode())            # 'Peter'


# Methods to set and get expiration time using (also using timedelta):
client.expire('name', 10)                                                                             # Expire in 10 seconds
expiration_time = client.ttl('name')
print(f'name gonna expire in {expiration_time} seconds')                                              # 'name gonna expire in 10 seconds'

in_a_week = datetime.timedelta(days=7)
client.expire('name', in_a_week)      
expiration_time = client.ttl('name')                                                                  # Value will expire in a week
print(f'name gonna expire in {expiration_time} seconds or {round(expiration_time/60/60/24)} days')    # 'name gonna expire in 604800 seconds or 7 days'


# Store python objects using pickle in redis:
python_var = {'Name': 'Peter', 'Age': 23, 'Job': None, 'Dream': 'Travelling'}
pickled_var = pickle.dumps(python_var)
client.set('python_var', pickled_var)
python_var = pickle.loads(client.get('python_var'))
print(python_var)                                                    # {'Name': 'Peter', 'Age': 23, 'Job': None, 'Dream': 'Travelling'}


# Another method to set expiration time:
client.set('bananas', 5, ex=10)
time.sleep(5)
expiration_time = client.ttl('bananas')
print(f'5 bananas gonna expire in {expiration_time} seconds')        # 5 bananas gonna expire in 10 seconds

client.set('bananas', 10, px=1000)
time.sleep(1)
expiration_time = client.ttl('bananas')
print(f'10 bananas gonna expire in {expiration_time} milliseconds')  # 10 bananas gonna expire in 1000 milliseconds


# Pipelines usage (increases the speed between client and server, helps to execute all commands at one time):
p = client.pipeline(transaction=False)
p.set('Somebody', 'Once')
p.expire('Somebody', 10)
time.sleep(3)
print(p.ttl('Somebody'))                          # Not gonna be 10 - 3 = 7 seconds because all comands in pipelines are executed at one time without any delay
results = p.execute()                             # Due to "transation=False" commands are not going to be executed automatically, also .execute() fetches the results
print(results)                                    # [True, True, 10] First two operations returned boolean, 10 - expiration time in seconds
p.close()                                         # Closing the pipeliene


with client.pipeline() as p:                      # "With" operator automatically closes the connection with pipeline, "transaction=True" by default
    p.set('Pet', 'Cat')
    p.expire('Pet', 10)
    time.sleep(2)
    p.ttl('Pet')                                  # Not gonna be 8 seconds because of using pipeline
    print(p.execute())                            # [True, True, 10] Again first two operation returned True ~ means success


"""
Other useful commands and information:

client.flushall()       -   deletes everything
client.exists(*names)   -   returns the number of elements that exist
client.keys()           -   returns the list of all names (keys)
pipeline.reset()        -   reset previous commands

"""
