from flask import Flask, request, jsonify
from chrome import infromwe, download

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/url', methods=['POST'])
def process_url():
    user_url = request.form.get('url')
    if not user_url:
        return jsonify({"success": False, "error": "No URL provided."})

    try:
        file_name = infromwe(user_url)
        if file_name:
            download(file_name)
            return jsonify({"success": True, "file_name": file_name})
        else:
            return jsonify({"success": False, "error": "File name could not be retrieved."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
