from flask import Flask, jsonify
import psutil
import os
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def check_quota():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    cpu_quota = float(os.environ.get('CPU_QUOTA', 100))
    memory_quota = float(os.environ.get('MEMORY_QUOTA', 100))
    
    print(f"CPU: {cpu}% (квота: {cpu_quota}%) | Пам'ять: {memory}% (квота: {memory_quota}%)")
    
    alerts = []
    if cpu > cpu_quota:
        alerts.append(f"Перевищено CPU: {cpu}% > {cpu_quota}%")
    if memory > memory_quota:
        alerts.append(f"Перевищено пам'ять: {memory}% > {memory_quota}%")
    
    if alerts:
        print("Увага: " + "; ".join(alerts))

scheduler = BackgroundScheduler()
scheduler.add_job(check_quota, 'interval', minutes=5)
scheduler.start()

@app.route('/')
def home():
    return "Дослідження квот хмарних обчислень"

@app.route('/metrics')
def metrics():
    return jsonify({
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)