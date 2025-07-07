from flask import Flask, jsonify, request, abort
import logging
import random
import time

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
)

log_messages = {
    'debug': [
        "Cache miss on user profile",
        "Retrying request to internal service",
        "Debugging session started for user ID 123"
    ],
    'info': [
        "User successfully logged in",
        "Background job completed",
        "Service health check passed"
    ],
    'warning': [
        "High memory usage detected",
        "Slow response from payment gateway",
        "JWT token about to expire"
    ],
    'error': [
        "Database connection failed",
        "Redis timeout during session fetch",
        "Unhandled exception occurred"
    ],
    'critical': [
        "Service crash: panic in main loop",
        "Payment processing failed for order #9876",
        "Security breach detected – shutting down API"
    ]
}

http_errors = [
    (401, "Unauthorized: Missing or invalid token"),
    (403, "Forbidden: User does not have access"),
    (404, "Not Found: Resource does not exist"),
    (500, "Internal Server Error: Unexpected exception"),
    (502, "Bad Gateway: Upstream service not responding"),
]


def generate_random_log():
    level = random.choice(list(log_messages.keys()))
    message = random.choice(log_messages[level])
    app.logger.log(getattr(logging, level.upper()), message)

    log_result = {"message": message, "level": level}

    if random.random() < 0.2:
        code, err_msg = random.choice(http_errors)
        error_log = f"HTTP {code} - {err_msg}"
        app.logger.error(error_log)
        log_result["http_error"] = {"code": code, "message": err_msg}

    return log_result


@app.route('/')
def index():
    return '''
    <h1>Flask Logging App</h1>
    <ul>
        <li><a href="/generate-log">Generate one log</a></li>
        <li><a href="/generate-massive-logs?count=100">Generate 100 logs</a></li>
        <li><a href="/generate-error">Generate random HTTP error</a></li>
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

    return jsonify({"generated": len(logs), "logs": logs})


@app.route('/generate-error')
def generate_error():
    code, message = random.choice(http_errors)
    app.logger.error(f"HTTP {code} - {message}")
    abort(code, description=message)


@app.errorhandler(Exception)
def handle_exception(e):
    code = getattr(e, 'code', 500)
    return jsonify({"error": str(e)}), code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
