from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import redis
import os
app = Flask(__name__)
socketio = SocketIO(app)
redis_client = redis.Redis(password=os.environ['REDIS_PASSWORD'])
pubsub_channels = ['myagentshellchannel', 'myagentchannel']

#redis.Redis()

def redis_subscriber():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(*pubsub_channels)
    for message in pubsub.listen():
        if message['type'] == 'message':
            channel = message['channel'].decode()
            print('Emitting', channel, message['data'])
            socketio.emit(channel, {'data': message['data'].decode()})

@app.route('/index1')
def index():
    return render_template('index.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')

@app.route('/agentchannel')
def agentchannel():
    return render_template('agentchannel.html')


if __name__ == '__main__':
    threading.Thread(target=redis_subscriber).start()

    #socketio.run(app, port=5000, debug=True)
    # should be available to outside so 0.0.0.0
    socketio.run(app, host='0.0.0.0', port=1234, debug=True)
