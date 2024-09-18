import requests
from core import settings

API_URL = settings.API_URL

def get_users():
    try:
        response = requests.get(f"{API_URL}/user/?all=true&operator=%3D&skip=0&limit=100")
        return response.json()
    except Exception as e:
        return ["dia"]


def create_user(user_data):
    response = requests.post(f"{API_URL}/user", json=user_data)
    return response.json()

def get_roles():
    response = requests.get(f"{API_URL}/role/?all=true&operator=%3D&skip=0&limit=100")
    return response.json()

def create_role(role_data):
    response = requests.post(f"{API_URL}/role", json=role_data)
    return response.json()
