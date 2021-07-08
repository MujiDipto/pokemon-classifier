from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.applications import imagenet_utils
from sklearn.metrics import confusion_matrix
import itertools
import os
import shutil
import random
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import cv2
from PIL import Image


new_model = load_model('pokemon_pred_mobilenet.h5')

label_dict = {'Abra': 0,
 'Aerodactyl': 1,
 'Alakazam': 2,
 'Alolan Sandslash': 3,
 'Arbok': 4,
 'Arcanine': 5,
 'Articuno': 6,
 'Beedrill': 7,
 'Bellsprout': 8,
 'Blastoise': 9,
 'Bulbasaur': 10,
 'Butterfree': 11,
 'Caterpie': 12,
 'Chansey': 13,
 'Charizard': 14,
 'Charmander': 15,
 'Charmeleon': 16,
 'Clefable': 17,
 'Clefairy': 18,
 'Cloyster': 19,
 'Cubone': 20,
 'Dewgong': 21,
 'Diglett': 22,
 'Ditto': 23,
 'Dodrio': 24,
 'Doduo': 25,
 'Dragonair': 26,
 'Dragonite': 27,
 'Dratini': 28,
 'Drowzee': 29,
 'Dugtrio': 30,
 'Eevee': 31,
 'Ekans': 32,
 'Electabuzz': 33,
 'Electrode': 34,
 'Exeggcute': 35,
 'Exeggutor': 36,
 'Farfetchd': 37,
 'Fearow': 38,
 'Flareon': 39,
 'Gastly': 40,
 'Gengar': 41,
 'Geodude': 42,
 'Gloom': 43,
 'Golbat': 44,
 'Goldeen': 45,
 'Golduck': 46,
 'Golem': 47,
 'Graveler': 48,
 'Grimer': 49,
 'Growlithe': 50,
 'Gyarados': 51,
 'Haunter': 52,
 'Hitmonchan': 53,
 'Hitmonlee': 54,
 'Horsea': 55,
 'Hypno': 56,
 'Ivysaur': 57,
 'Jigglypuff': 58,
 'Jolteon': 59,
 'Jynx': 60,
 'Kabuto': 61,
 'Kabutops': 62,
 'Kadabra': 63,
 'Kakuna': 64,
 'Kangaskhan': 65,
 'Kingler': 66,
 'Koffing': 67,
 'Krabby': 68,
 'Lapras': 69,
 'Lickitung': 70,
 'Machamp': 71,
 'Machoke': 72,
 'Machop': 73,
 'Magikarp': 74,
 'Magmar': 75,
 'Magnemite': 76,
 'Magneton': 77,
 'Mankey': 78,
 'Marowak': 79,
 'Meowth': 80,
 'Metapod': 81,
 'Mew': 82,
 'Mewtwo': 83,
 'Moltres': 84,
 'MrMime': 85,
 'Muk': 86,
 'Nidoking': 87,
 'Nidoqueen': 88,
 'Nidorina': 89,
 'Nidorino': 90,
 'Ninetales': 91,
 'Oddish': 92,
 'Omanyte': 93,
 'Omastar': 94,
 'Onix': 95,
 'Paras': 96,
 'Parasect': 97,
 'Persian': 98,
 'Pidgeot': 99,
 'Pidgeotto': 100,
 'Pidgey': 101,
 'Pikachu': 102,
 'Pinsir': 103,
 'Poliwag': 104,
 'Poliwhirl': 105,
 'Poliwrath': 106,
 'Ponyta': 107,
 'Porygon': 108,
 'Primeape': 109,
 'Psyduck': 110,
 'Raichu': 111,
 'Rapidash': 112,
 'Raticate': 113,
 'Rattata': 114,
 'Rhydon': 115,
 'Rhyhorn': 116,
 'Sandshrew': 117,
 'Sandslash': 118,
 'Scyther': 119,
 'Seadra': 120,
 'Seaking': 121,
 'Seel': 122,
 'Shellder': 123,
 'Slowbro': 124,
 'Slowpoke': 125,
 'Snorlax': 126,
 'Spearow': 127,
 'Squirtle': 128,
 'Starmie': 129,
 'Staryu': 130,
 'Tangela': 131,
 'Tauros': 132,
 'Tentacool': 133,
 'Tentacruel': 134,
 'Vaporeon': 135,
 'Venomoth': 136,
 'Venonat': 137,
 'Venusaur': 138,
 'Victreebel': 139,
 'Vileplume': 140,
 'Voltorb': 141,
 'Vulpix': 142,
 'Wartortle': 143,
 'Weedle': 144,
 'Weepinbell': 145,
 'Weezing': 146,
 'Wigglytuff': 147,
 'Zapdos': 148,
 'Zubat': 149
 }




app = Flask(__name__)

@app.route('/home')
def home():
   return render_template('home.html')



@app.route('/uploadPokemon')
def uploadPokemon():
    return render_template('uploadPokemon.html')



@app.route('/classifiedPokemon', methods = ['GET', 'POST'])
def classifiedPokemon():
    if request.method == 'POST':
       data = request.files['file']
       img = Image.open(request.files['file'])
       img = np.array(img)
       img = cv2.resize(img,(224,224))

       if len(img.shape)==2:
           img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGRA)

       if len(img.shape) > 2 and img.shape[2] == 4:
           #convert the image from RGBA2RGB
           img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

       preprocessed_image = prepare_image(img)
       predictions = new_model.predict(preprocessed_image)
       out = np.argmax(predictions)
       pokemon = list(label_dict.keys())[list(label_dict.values()).index(out)]
       return render_template('classifiedPokemon.html', pokemon = pokemon)



@app.route('/pokemonList')
def pokemonList():
    return render_template('pokemonList.html')


@app.route('/uploadOwn')
def uploadOwn():
    return render_template('uploadOwn.html')



@app.route('/classifiedOwn', methods = ['GET', 'POST'])
def classifiedOwn():
    if request.method == 'POST':
       data = request.files['file']
       img = Image.open(request.files['file'])
       img = np.array(img)
       img = cv2.resize(img,(224,224))

       if len(img.shape)==2:
           img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGRA)

       if len(img.shape) > 2 and img.shape[2] == 4:
           #convert the image from RGBA2RGB
           img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

       # a = img.shape
       # b = img.shape[2]

       preprocessed_image = prepare_image(img)
       predictions = new_model.predict(preprocessed_image)
       out = np.argmax(predictions)
       pokemon = list(label_dict.keys())[list(label_dict.values()).index(out)]
       return render_template('classifiedOwn.html', pokemon = pokemon)




@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'


def prepare_image(img):
    #img_path = 'pokemon-prediction/'
    # img = image.load_img(file, target_size=(224, 224))
    # print(type(img))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)




if __name__ == '__main__':
   app.run(debug = True)