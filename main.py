import flask_excel as excel
from flask import Flask, request, jsonify
import mail

app = Flask(__name__)

excel.init_excel(app)


@app.route('/v1/upload', methods=["POST"])
def upload():
    if request.method == 'POST':
        data = request.get_array(field_name='file')
        for user in data[1:]:
            email = user[0]
            password = user[1]
            success = mail.copy_mail(email,password=password)
        return jsonify({"success": success})


if __name__ == '__main__':
    app.run()
