import requests

'''
Создать задачу
'''

data = {
    'title': 'Встретиться с коллегой',
    'body': 'Встретиться с коллегой в 7 часов вечера',
    'categories': ['Личное']
}
responce = requests.post('http://127.0.0.1:8000/create_task', json=data)
print(responce.json())

'''
Получить все задачи
'''
import requests
responce = requests.get('http://127.0.0.1:8000/get_tasks')
print(responce.json())

'''
Получить задачу по id
'''
import requests
responce = requests.get('http://127.0.0.1:8000/get_task/1')
print(responce.json())

'''
Удалить задачу по идентификатору
'''
import requests
responce = requests.delete('http://127.0.0.1:8000/delete_task/1')
print(responce.json())


'''
Получайте задачи по категориям
'''
import requests
responce = requests.get("http://127.0.0.1:8000/get_tasks_by_categories/Личное")
print(responce.json())

'''
Обновить статус задачи
'''
import requests
responce = requests.post("http://127.0.0.1:8000/update_task_status/1")
print(responce.json())