from flask import Flask, jsonify, request
import logging
import random
import time

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
)

log_levels = ['debug', 'info', 'warning', 'error', 'critical']

def generate_random_log():
    level = random.choice(log_levels)
    message = f"To jest przykładowy log na poziomie {level.upper()}"

    if level == 'debug':
        app.logger.debug(message)
    elif level == 'info':
        app.logger.info(message)
    elif level == 'warning':
        app.logger.warning(message)
    elif level == 'error':
        app.logger.error(message)
    elif level == 'critical':
        app.logger.critical(message)

    return {"message": message, "level": level}


@app.route('/')
def index():
    return '''
    <h1>Flask Logging App</h1>
    <ul>
        <li><a href="/generate-log">Wygeneruj jeden log</a></li>
        <li><a href="/generate-massive-logs?count=100">Wygeneruj 100 logów</a></li>
    </ul>
    '''


@app.route('/generate-log')
def generate_log():
    return jsonify(generate_random_log())


@app.route('/generate-massive-logs')
def generate_massive_logs():
    try:
        count = int(request.args.get("count", 100))
    except ValueError:
        count = 100

    logs = []
    for _ in range(count):
        logs.append(generate_random_log())
        time.sleep(0.01)  

    return jsonify({"generated": len(logs)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
