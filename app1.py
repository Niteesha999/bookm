from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import urllib.parse

app = Flask(__name__)
CORS(app)

# Connection string
trusted_conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=your_database;TRUSTED_CONNECTION=yes'
encoded_conn_str = urllib.parse.quote_plus(trusted_conn_str)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=' + encoded_conn_str
db = SQLAlchemy(app)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookmark_name = db.Column(db.String(100))
    client = db.Column(db.String(500))
    product = db.Column(db.String(500))
    client_segment = db.Column(db.String(500))

@app.route('/save', methods=['POST'])
def save_bookmark():
    data = request.json
    new_bookmark = Bookmark(
        bookmark_name=data['bookmarkName'],
        client=','.join(data['client']),
        product=','.join(data['product']),
        client_segment=','.join(data['clientSegment'])
    )
    db.session.add(new_bookmark)
    db.session.commit()
    return jsonify({'message': 'Bookmark saved successfully!'})

@app.route('/update/<int:id>', methods=['PUT'])
def update_bookmark(id):
    data = request.json
    bookmark = Bookmark.query.get(id)
    if bookmark:
        bookmark.client = ','.join(data['client'])
        bookmark.product = ','.join(data['product'])
        bookmark.client_segment = ','.join(data['clientSegment'])
        db.session.commit()
        return jsonify({'message': 'Bookmark updated successfully!'})
    return jsonify({'message': 'Bookmark not found!'}), 404

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_bookmark(id):
    bookmark = Bookmark.query.get(id)
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({'message': 'Bookmark deleted successfully!'})
    return jsonify({'message': 'Bookmark not found!'}), 404

@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    bookmarks = Bookmark.query.all()
    result = []
    for bookmark in bookmarks:
        result.append({
            'id': bookmark.id,
            'bookmarkName': bookmark.bookmark_name,
            'client': bookmark.client.split(','),
            'product': bookmark.product.split(','),
            'clientSegment': bookmark.client_segment.split(',')
        })
    return jsonify(result)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
