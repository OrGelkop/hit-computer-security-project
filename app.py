from flask import Flask, render_template, request, Response
from db import DatabaseManagement
import management
import ezgmail
import os
import sys

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')


DEBUG_MODE = os.environ.get('DEBUG_MODE', False)

@app.route('/', methods=['GET'])
def redirect_to_index():
    db_object = DatabaseManagement()
    games = db_object.fetch_preview()
    games_count = db_object.fetch_count()
    return render_template("index.html", games=games, games_count=games_count)


@app.route('/all_games', methods=['POST'])
def list_all_games():
    if request.method == 'POST':
        result = request.form
        try:
            db_object = DatabaseManagement()
            all_games = db_object.fetch_all()
            games_count = db_object.fetch_count()
            user = db_object.check_subscription(result['allgamesmail'])
            if user[0][0] == 1:
                status_code = 0
            else:
                status_code = 1
        except Exception as e:
            print(e)
            status_code = 2
        finally:
            return render_template("all_games.html", games=all_games, games_count=games_count, status_code=status_code)


@app.route('/request', methods=['POST'])
def game_request():
    if request.method == 'POST':
        result = request.form
        try:
            db_object = DatabaseManagement()
            is_subscribed = db_object.check_subscription(result['gamemail'])[0][0]
            if is_subscribed == 1:  # Checks if user subscribed
                is_valid = management.check_game_request(result['gamelink'])
                if is_valid != "":  # Checks if URL is for playstation store
                    db_object.insert_game(result['gamename'], result['gamelink'], is_valid)
                    msg_body = "Successfully added game to the tracking list\nGame name - {}\nGame URL - {}"\
                        .format(result['gamename'], result['gamelink'])
                else:
                    return "Please make sure that the given URL is valid and try again."
            else:
                return "Only subscribed users can request tracking games."

            if result['gamemail'] != os.environ['ADMIN_ADDRESS']:
                ezgmail.send(result['gamemail'], 'Cheap Play - Game tracking request', msg_body, sender='Cheap Play')
            msg_body = msg_body + "\nRequestor mail address - {}".format(result['gamemail'])
            ezgmail.send(ezgmail.EMAIL_ADDRESS, 'Cheap Play - Game tracking request', msg_body, sender='Cheap Play')
            return "Game successfully added to tracking list!"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)
            if "duplicate" in str(e):
                return "This game is already tracked."
            else:
                return "Game tracking request failed, please try again later."


@app.route('/subscribe', methods=['POST'])
def subscribe_request():
    if request.method == 'POST':
        result = request.form
        try:
            msg_body = "New subscription request\nFull name - {}\nEmail address - {}\nPhone number - {}"\
                .format(result['name'], result['email'], result['phone'])
            ezgmail.send(ezgmail.EMAIL_ADDRESS, 'Cheap Play - Subscribing request', msg_body, sender='Cheap Play')

            return "Subscribing request sent successfully!"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)
            return "Subscribing request failed, please try again later."


@app.route('/test_db', methods=['GET'])
def test_db():
    db_object = DatabaseManagement()
    count = db_object.get_users_count()[0][0]
    return Response(str(count), 200)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG_MODE)
