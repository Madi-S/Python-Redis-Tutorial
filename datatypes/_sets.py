import redis


# In this tutorial we are gonna cover following commands for sets:

with redis.Redis(host='127.0.0.1', port=6379) as client:
