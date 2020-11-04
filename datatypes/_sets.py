
import redis

mylist = list() # To make sure you understand everything corresponding commands in redis for lists will be shown with python lists' commands


# In this tutorial we are gonna cover following commands for lists:

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
