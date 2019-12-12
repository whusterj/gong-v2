from flask import Flask, jsonify, request
import pigpio
import time
from datetime import datetime, timedelta
import shelve

from do_async import do_async

# globals
app = Flask(__name__)

SECRET = 'dK9gMGd2YPbMuuPzBxr7K4stACcx43Rv'
SLACK_SECRET = '6uznUQ7MzcrFOAOXflUrpQZX'
DAILY_RING_LIMIT = 150

db_name = 'gong'

# Initialize RPi GPIO
servo_pin = 7

right_cycle = 1000
middle_cycle = 1500
left_cycle = 2000

pi = pigpio.pi()


def init_db():
    print('Initializing gong database')
    s = shelve.open(db_name)
    try:
        s['entries']
    except KeyError:
        s['entries'] = []
    s.close()


def ring_gong(num_rings=1):
    for _ in range(0, num_rings):
        pi.set_servo_pulsewidth(servo_pin, left_cycle)
        time.sleep(0.2)
    
        pi.set_servo_pulsewidth(servo_pin, right_cycle)
        time.sleep(0.13)
    
        pi.set_servo_pulsewidth(servo_pin, left_cycle)
        time.sleep(0.1)
    

def recent_rings(user_name):
    one_day_ago = datetime.now() - timedelta(days=1)
    s = shelve.open(db_name, flag='r')
    try:
        entries = s['entries']
        recent_user_rings = [e[1] for e in entries
                             if e[0]==user_name and e[2]>=one_day_ago]
        return sum(x for x in recent_user_rings)
    finally:
        s.close()


def add_ring_entry(user_name, count, timestamp=datetime.now()):
    s = shelve.open(db_name)
    try:
        entries = s['entries']
        entries.append((user_name, count, timestamp, ))
        s['entries'] = entries
    finally:
        s.close()


@app.route('/', methods=['POST'])
def index():
    given_token = request.form.get('token')
    num_rings = int(request.form.get('num_rings', 5))
    if given_token == SECRET:
        ring_gong(num_rings)
        return 'Rang {0} times'.format(num_rings)
    else:
        return 'Token not recognized or provided.'


@app.route('/slack-command/', methods=['GET', 'POST'])
def slack_command():
    """Endpoint to handle the gong-ringing Slack 'slash command'.

    This command is configured in the Slack's admin settings.
    At Aspire, we set up the command to be used like so:

        /gongme [text]

    The command accepts just one integer argument: `num_rings`, which
    must be between 1 and 50. Larger numbers will be clamped to fifty
    and negative numbers are denied and the gong will not ring.

    Text arguments are allowed, and will cause the gong to ring five times.
    """

    if request.method == 'GET':
        return 'OK'

    elif request.method == 'POST':

        # Collect POST data
        given_token = request.form.get('token')
        user_name = request.form.get('user_name')
        text = request.form.get('text')
        command_args = text.split()

        # Validate Slack's secret token.
        if not given_token == SLACK_SECRET:
            return 'FORBIDDEN'

        # Validate ring count input
        try:
            num_rings = int(command_args[0])
        except (IndexError, ValueError):
            num_rings = 5
        if num_rings < 0:
            msg = 'Yeah, that\'s not gonna happen'
        elif num_rings > 50:
            msg = 'That\'s obnoxious. I\'ll just ring it 50 times.'
            num_rings = 50
        else:
            msg = 'Oh, yeaaah!'

        # Check if the user still has rings available today
        recent_ring_count = recent_rings(user_name)
        if recent_ring_count >= DAILY_RING_LIMIT:
            return jsonify({
                'text': 'No! You\'ve hit your gong limit for today!'
            })
        
        # Clamp ring count to daily limit
        if (recent_ring_count + num_rings) >= DAILY_RING_LIMIT:
            num_rings = DAILY_RING_LIMIT - recent_ring_count
            msg += ' (no more rings for you today)'

        # Ring the gong and record the ring in the shelf
        do_async(ring_gong, num_rings)
        add_ring_entry(user_name, num_rings)

        return jsonify({
            'response_type': 'in_channel',
            'text': msg,
            'attachments': [
                {
                    'text': '{0} rang the gong {1} times'.format(user_name, num_rings)
                }
            ]
        })


if __name__ == "__main__":
    app.run()
