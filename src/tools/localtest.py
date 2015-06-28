__author__ = 'jarrah'
from src.db import service

print(service.select_rows_limit('circle_interest', 0, 'user_id', 'circle_id'))
service.switch_table_row('circle_interest', ['user_id', 'circle_id'], [2, 2], 'user_id=%s and circle_id=%s', [2, 2])
