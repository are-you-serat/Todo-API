# Todo-API
Typical to-do list api written in fastapi

This api uses postgresql, but you can change this in the code. This API implements functions such as: 
1) create_task
2) get_tasks
3) get_task_by_id
4) delete_task_by_id
5) get_tasks_by_categories
6) update_task_status

To see what each function does, simply run the api on localhost and read the swagger documentation.

# Installation
1) Clone repo
2) Install the dependencies with the command ```pip install -r requirements.txt```
3) Go to the directory with api.py with the command ```cd fastapi```
4) Run ```fastapi dev api.py```.
