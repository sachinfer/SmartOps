# app.py
from fastapi import FastAPI, HTTPException, Query
import logging
import time
import random

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

@app.get("/")
def read_root():
    logging.info("Root endpoint accessed")
    return {"message": "Hello SmartOps!!!"}

@app.get("/health")
def health():
    logging.info("Health check OK")
    return {"status": "ok"}

@app.get("/status")
def status():
    logging.info("Status endpoint accessed")
    return {"status": "running", "uptime": random.randint(100, 10000)}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    if user_id < 0:
        logging.warning(f"Invalid user id: {user_id}")
        raise HTTPException(status_code=400, detail="Invalid user id")
    logging.info(f"User {user_id} profile accessed")
    return {"user_id": user_id, "name": f"User{user_id}"}

@app.post("/register")
def register(username: str = Query(...)):
    logging.info(f"User registered: {username}")
    return {"message": f"User {username} registered"}

@app.put("/user/{user_id}/update")
def update_user(user_id: int, name: str = Query(...)):
    logging.info(f"User {user_id} updated to {name}")
    return {"user_id": user_id, "name": name}

@app.delete("/user/{user_id}/delete")
def delete_user(user_id: int):
    logging.warning(f"User {user_id} deleted")
    return {"message": f"User {user_id} deleted"}

@app.get("/search")
def search(q: str = Query(...)):
    logging.info(f"Search performed: {q}")
    return {"results": [q, q[::-1]]}

@app.post("/login")
def login(username: str = Query(...)):
    if username == "admin":
        logging.info(f"Admin login attempt: {username}")
        return {"message": "Welcome admin!"}
    logging.info(f"User login: {username}")
    return {"message": f"Welcome {username}!"}

@app.post("/logout")
def logout(username: str = Query(...)):
    logging.info(f"User logout: {username}")
    return {"message": f"Goodbye {username}!"}

@app.get("/items")
def list_items():
    logging.info("Items listed")
    return {"items": [f"item{i}" for i in range(10)]}

@app.post("/items")
def add_item(name: str = Query(...)):
    logging.info(f"Item added: {name}")
    return {"item": name, "status": "added"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id % 5 == 0:
        logging.error(f"Item {item_id} not found!")
        raise HTTPException(status_code=404, detail="Item not found")
    logging.info(f"Item {item_id} accessed")
    return {"item_id": item_id, "value": random.random()}

@app.put("/items/{item_id}/update")
def update_item(item_id: int, name: str = Query(...)):
    logging.info(f"Item {item_id} updated to {name}")
    return {"item_id": item_id, "name": name}

@app.delete("/items/{item_id}/delete")
def delete_item(item_id: int):
    logging.warning(f"Item {item_id} deleted")
    return {"message": f"Item {item_id} deleted"}

@app.post("/order")
def place_order(item_id: int = Query(...), user_id: int = Query(...)):
    order_id = random.randint(1000, 9999)
    logging.info(f"Order {order_id} placed for item {item_id} by user {user_id}")
    return {"order_id": order_id, "status": "placed"}

@app.get("/order/{order_id}")
def get_order(order_id: int):
    status = random.choice(["processing", "shipped", "delivered", "cancelled"])
    logging.info(f"Order {order_id} status checked: {status}")
    return {"order_id": order_id, "status": status}

@app.post("/order/{order_id}/cancel")
def cancel_order(order_id: int):
    logging.warning(f"Order {order_id} cancelled")
    return {"order_id": order_id, "status": "cancelled"}

@app.get("/admin/stats")
def admin_stats():
    stats = {"users": random.randint(10, 100), "orders": random.randint(10, 100), "items": 10}
    logging.info("Admin stats viewed")
    return stats

@app.get("/admin/logs")
def admin_logs():
    logging.info("Admin logs viewed")
    return {"logs": ["log1", "log2", "log3"]}

@app.get("/unstable")
def unstable():
    outcome = random.choice([200, 400, 500, "timeout"])
    if outcome == 200:
        logging.info("Unstable endpoint: 200 OK")
        return {"message": "OK"}
    elif outcome == 400:
        logging.warning("Unstable endpoint: 400 Bad Request")
        raise HTTPException(status_code=400, detail="Bad request")
    elif outcome == 500:
        logging.error("Unstable endpoint: 500 Internal Server Error")
        raise HTTPException(status_code=500, detail="Internal server error")
    else:
        logging.warning("Unstable endpoint: timeout")
        time.sleep(3)
        raise HTTPException(status_code=504, detail="Gateway Timeout")

@app.post("/auth/login")
def auth_login(username: str = Query(...)):
    logging.info(f"Auth login: {username}")
    return {"token": f"token-{username}"}

@app.post("/auth/logout")
def auth_logout(username: str = Query(...)):
    logging.info(f"Auth logout: {username}")
    return {"message": f"Logged out {username}"}

@app.post("/auth/refresh")
def auth_refresh(token: str = Query(...)):
    logging.info(f"Auth token refreshed: {token}")
    return {"token": token + "-refreshed"}

@app.get("/slow")
def slow():
    logging.info("Slow endpoint called")
    time.sleep(2)
    return {"message": "That was slow!"}

@app.get("/fail")
def fail():
    logging.error("Fail endpoint triggered")
    raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/error")
def error():
    logging.error("This is a test error log")
    return {"error": "Test error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
