import requests
import time
import random

BASE_URL = "http://localhost:8081"

endpoints = [  # (method, path, params)
    ("GET", "/", {}),
    ("GET", "/health", {}),
    ("GET", "/status", {}),
    ("GET", "/user/{user_id}", lambda: {"user_id": random.randint(-2, 20)}),
    ("POST", "/register", lambda: {"username": f"user{random.randint(1,100)}"}),
    ("PUT", "/user/{user_id}/update", lambda: {"user_id": random.randint(1, 20), "name": f"User{random.randint(1,100)}"}),
    ("DELETE", "/user/{user_id}/delete", lambda: {"user_id": random.randint(1, 20)}),
    ("GET", "/search", lambda: {"q": random.choice(["test", "admin", "item", "error", "slow"])}),
    ("POST", "/login", lambda: {"username": random.choice(["admin", f"user{random.randint(1,100)}"])}),
    ("POST", "/logout", lambda: {"username": f"user{random.randint(1,100)}"}),
    ("GET", "/items", {}),
    ("POST", "/items", lambda: {"name": f"item{random.randint(1,100)}"}),
    ("GET", "/items/{item_id}", lambda: {"item_id": random.randint(0, 20)}),
    ("PUT", "/items/{item_id}/update", lambda: {"item_id": random.randint(1, 20), "name": f"Item{random.randint(1,100)}"}),
    ("DELETE", "/items/{item_id}/delete", lambda: {"item_id": random.randint(1, 20)}),
    ("POST", "/order", lambda: {"item_id": random.randint(1, 20), "user_id": random.randint(1, 20)}),
    ("GET", "/order/{order_id}", lambda: {"order_id": random.randint(1000, 9999)}),
    ("POST", "/order/{order_id}/cancel", lambda: {"order_id": random.randint(1000, 9999)}),
    ("GET", "/admin/stats", {}),
    ("GET", "/admin/logs", {}),
    ("GET", "/unstable", {}),
    ("POST", "/auth/login", lambda: {"username": f"user{random.randint(1,100)}"}),
    ("POST", "/auth/logout", lambda: {"username": f"user{random.randint(1,100)}"}),
    ("POST", "/auth/refresh", lambda: {"token": f"token-user{random.randint(1,100)}"}),
    ("GET", "/slow", {}),
    ("GET", "/fail", {}),
    ("GET", "/error", {}),
    # Invalid endpoints for 404s
    ("GET", "/non-existent-route", {}),
    ("GET", "/missing", {}),
    ("GET", "/doesnotexist", {}),
    ("GET", "/bad", {}),
    ("GET", "/404", {}),
    ("GET", "/random", {}),
]

TOTAL_REQUESTS = 2000

for i in range(TOTAL_REQUESTS):
    method, path, params = random.choice(endpoints)
    # Replace path params
    if callable(params):
        p = params()
        for k, v in p.items():
            if f"{{{k}}}" in path:
                path = path.replace(f"{{{k}}}", str(v))
        query = {k: v for k, v in p.items() if f"{{{k}}}" not in path}
    else:
        query = {}
    url = BASE_URL + path
    try:
        if method == "GET":
            r = requests.get(url, params=query)
        elif method == "POST":
            r = requests.post(url, params=query)
        elif method == "PUT":
            r = requests.put(url, params=query)
        elif method == "DELETE":
            r = requests.delete(url, params=query)
        else:
            continue
        print(f"{i+1}: {method} {url} {query} -> {r.status_code}")
    except Exception as e:
        print(f"{i+1}: {method} {url} {query} -> ERROR: {e}")
    time.sleep(0.005)

print(f"Generated {TOTAL_REQUESTS} requests for log testing.") 