from flask import Flask, jsonify, request, redirect

import os
from werkzeug.utils import secure_filename
import urllib.request
from werkzeug.utils import secure_filename

from product import products

UPLOAD_FOLDER = 'C:/uploads'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ping')
def ping():
  return jsonify({"message":"Pong!"})

@app.route('/products', methods=['GET'])
def getProducts():
  return jsonify(products)

@app.route('/products/<string:product_name>', methods=['GET'])
def getProductById(product_name):
  productFound = [product for product in products if product['name'] == product_name]
  if (len(productFound) > 0):
    return jsonify(productFound[0])
  
  return jsonify({"message": "Propducto no encontrado"})

@app.route('/products', methods=['POST'])
def addProduct():
  print(request.json)
  product = {
    "name": request.json('name'),
    "price": request.json('price'),
    "quantity": request.json('quantity')
  }

  products.append(product)

  return jsonify({"message": "Producto agregado satisfactoriamente", "products": products})

@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):

  return jsonify()

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp

if __name__ == '__main__':
  app.run(debug=True, port=5000)