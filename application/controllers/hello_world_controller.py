from application import app


@app.route('/test', methods=['GET'])
def hello_world_test():
    return 'Hello, world!'
