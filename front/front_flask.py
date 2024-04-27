from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import redis
import os
app = Flask(__name__)
socketio = SocketIO(app)
redis_client = redis.Redis(password=os.environ['REDIS_PASSWORD'])
redis_pubsub_channel='myagentshellchannel'

#redis.Redis()

def redis_subscriber():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(redis_pubsub_channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            print('Emitting', message['data'])
            socketio.emit('new_message', {'data': message['data'].decode()})

@app.route('/index1')
def index():
    return render_template('index.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')


if __name__ == '__main__':
    threading.Thread(target=redis_subscriber).start()

    #socketio.run(app, port=5000, debug=True)
    # should be available to outside so 0.0.0.0
    socketio.run(app, host='0.0.0.0', port=1234, debug=True)
