__author__ = 'jarrah'
from src.db import service

<<<<<<< HEAD
# service.insert_follow(1, 11)
# service.insert_follow(1, 20)
# service.insert_follow(1, 5)

service.insert_moment_comment(1, 1, 1, 'reply')
print(service.select_moment_comment(1))
=======
print(service.select_rows_limit('circle_interest', 0, 'user_id', 'circle_id'))
service.switch_table_row('circle_interest', ['user_id', 'circle_id'], [2, 2], 'user_id=%s and circle_id=%s', [2, 2])
>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b
