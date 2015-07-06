__author__ = 'jarrah'
from src.db import service

# service.insert_follow(1, 11)
# service.insert_follow(1, 20)
# service.insert_follow(1, 5)

service.insert_moment_comment(1, 1, 1, 'reply')
print(service.select_moment_comment(1))
