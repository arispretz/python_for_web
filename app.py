# let's import the flask
from flask import Flask, render_template, request, redirect, url_for
import os # importing operating system module
import pymongo
from environs import Env
from bson.objectid import ObjectId # importing ObjectId
import re
from collections import Counter

# Create an instance of the `Env` class
env = Env()

# Cargar las variables de entorno desde el archivo .env
env.read_env()

'''# Acceder a las variables de entorno cargadas
my_variable = env('MY_VARIABLE')'''

# Obtener el URI de MongoDB de las variables de entorno
mongodb_uri = env("MONGODB_URI")
client = pymongo.MongoClient(mongodb_uri)

# Creating database
db = client.text_analyzer
# Creating students collection and inserting a document
db.friends.insert_one({'name': 'Ariana', 'country': 'Argentina', 'city': 'San Lorenzo', 'age': 44})
print(client.list_database_names())

friends = [
        {'name':'David','country':'UK','city':'London','age':34},
        {'name':'John','country':'Sweden','city':'Stockholm','age':28},
        {'name':'Sam','country':'Finland','city':'Helsinki','age':25},
    ]
for friend in friends:
    db.friends.insert_one(friend)
    
db = client['text_analyzer'] # accessing the database
friends = db.friends.find_one()
print(friend)

db = client['text_analyzer'] # accessing the database
friend = db.friends.find_one({'_id': ObjectId('5df68a23f106fe2d315bbc8c')})
print(friend)

db = client['text_analyzer'] # accessing the database
friends = db.friends.find()
for friend in friends:
    print(friend)

db = client['text_analyzer'] # accessing the database
friends = db.friends.find({}, {"_id":0,  "name": 1, "country":1}) # 0 means not include and 1 means include
for friend in friends:
    print(friend)


db = client['text_analyzer'] # accessing the database
query = {
    "country":"Finland"
}
friends = db.friends.find(query)

for friend in friends:
    print(friend)   
    
db = client['text_analyzer'] # accessing the database
query = {
    "city":"Helsinki"
}
friends = db.friends.find(query)
for friend in friends:
    print(friend)
    
db = client['text_analyzer'] # accessing the database
query = {
    "country":"Finland",
    "city":"Helsinki"
}
friends = db.friends.find(query)
for friend in friends:
    print(friend)
    
db = client['text_analyzer'] # accessing the database
query = {"age":{"$gt":30}}
friends = db.friends.find(query)
for friend in friends:
    print(friend)

db = client['text_analyzer'] # accessing the database
query = {"age":{"$gt":30}}
friends = db.friends.find(query)
for friend in friends:
    print(friend)
    
db = client['text_analyzer'] # accessing the database
db.friends.find().limit(3)

db = client['text_analyzer'] # accessing the database
friends = db.friends.find().sort('name')
for friend in friends:
    print(friend)

friends = db.friends.find().sort('name',-1)
for friend in friends:
    print(friend)

friends = db.friends.find().sort('age')
for friends in friends:
    print(friend)

friends = db.friends.find().sort('age',-1)
for friend in friends:
    print(friend)
    
db = client['text_analyzer'] # accessing the database

query = {'age':44}
new_value = {'$set':{'age':45}}

db.friends.update_one(query, new_value)
# lets check the result if the age is modified
for friend in db.friends.find():
    print(friend)
    
# When we want to update many documents at once we use update_many() method.
db = client['text_analyzer'] # accessing the database

query = {'name':'John'}
db.friends.delete_one(query)

for friend in db.friends.find():
    print(friend)
# lets check the result if the age is modified
for friend in db.friends.find():
    print(friend)
    
'''db = client['text_analyzer'] # accessing the database
db.friends.drop()'''



app = Flask(__name__)
# to stop caching static file
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



def cleaning_text(text):
    # Convertir todas las letras a minúsculas
    text = text.lower()
    # Eliminar caracteres no alfabéticos, números y espacios adicionales
    text = re.sub(r'[^a-záéíóúüñ\s]', '', text)
    # Eliminar espacios adicionales
    text = re.sub(r'\s+', ' ', text)
    return text.strip()  # Eliminar espacios al principio y al final

text = "Este es un ejemplo de texto con 123 números y signos de puntuación!!!"
cleaned_text = cleaning_text(text)
print("Cleaned Text:", cleaned_text)



def counting_words_regex(text):
    words = re.findall(r'\w+', text)
    return len(words)

text = "Este es un ejemplo de texto para contar palabras en Python"
result = counting_words_regex(text)
print("Amount of Words:", result)


def counting_characters(text):
    return len(text)

text = "Este es un ejemplo de texto para contar caracteres en Python"
result = counting_characters(text)
print("Amount of Characters:", result)



def more_frequent_words(text, amount=5):
    words = re.findall(r'\w+', text.lower())
    count = Counter(words)
    return count.most_common(amount)

text = """
Este es un ejemplo de texto. Este texto tiene varias palabras, algunas de las cuales se repiten más que otras. 
Por ejemplo, la palabra "texto" se repite varias veces en este texto de ejemplo.
"""

result = more_frequent_words(text)
print("More Frequent Words:")
for word, frecuency in result:
    print(f"{word}: {frecuency} times")




@app.route('/') # this decorator create the home route
def home ():
    techs = ['HTML', 'CSS', 'Flask', 'Python']
    name = '30 Days Of Python Programming'
    return render_template('home.html', techs=techs, name = name, title = 'Home')

@app.route('/about')
def about():
    name = '30 Days Of Python Programming'
    return render_template('about.html', name = name, title = 'About')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/post', methods= ['GET','POST'])
def post():
    name = 'Text Analyzer'
    if request.method == 'GET':
         return render_template('post.html', name = name, title = name)
    if request.method =='POST':
        content = request.form['content']
        cleaned_text = cleaning_text(content)
        words_count = counting_words_regex(content)
        characters_count = counting_characters(content)
        frequent_words = more_frequent_words(content)
        return render_template('result.html', content=content, cleaned_text=cleaned_text, words_count=words_count, characters_count=characters_count, frequent_words=frequent_words)



if __name__ == '__main__':
    # for deployment
    # to make it work for both production and development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    
