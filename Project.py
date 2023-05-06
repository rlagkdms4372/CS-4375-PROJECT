# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EJ9DUv-zF9835gWN9JYVvyJvqBB19bat
"""

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score,confusion_matrix

class RNN:
  def __init__(self, dataFile):
    self.raw_input = pd.read_csv(dataFile)

  def preprocess(self, size, split_size):
    self.df = self.raw_input
    print(self.df)
    self.df = self.df.drop(['Adj Close', 'Volume'], axis = 1)
    #scaler = StandardScaler() #Standarization
    scaler = MinMaxScaler()
    self.df[['Open', 'High', 'Low', 'Close']] = scaler.fit_transform(self.df[['Open', 'High', 'Low', 'Close']])
    #print(self.df)
    self.open_df = self.df[['Open']]
    #print(self.open_df)
    self.close_df = self.df[['Close']]
    #print(self.close_df)
    # Remove null or NA values
    self.df.dropna(inplace = True)
    # Remove any redundant rows
    self.df.drop_duplicates(inplace = True)
    n = len(self.df)
    n_ratio = round(n * split_size)
    

    #Open
    self.open_df_train = self.open_df[:n_ratio]
    self.open_df_test = self.open_df[n_ratio:]

    #Close
    self.close_df_train = self.close_df[:n_ratio]
    self.close_df_test = self.close_df[n_ratio:]



    self.open_df_train = np.array(self.open_df_train)
    self.close_df_train = np.array(self.close_df_train)

    self.open_df_test = np.array(self.open_df_test)
    self.close_df_test = np.array(self.close_df_test)

    self.X_open_train = []
    self.y_open_train = []
    self.X_open_test = []
    self.y_open_test = []


    self.X_close_train = []
    self.y_close_train = []
    self.X_close_test = []
    self.y_close_test = []

################################OPEN############################################

    for i in range(len(self.open_df_train) - size):
      self.X_open_train.append(self.open_df_train[i : i + size])
      self.y_open_train.append(self.open_df_train[i + size])

    for i in range(len(self.open_df_test) - size):
      self.X_open_test.append(self.open_df_test[i : i + size])
      self.y_open_test.append(self.open_df_test[i + size])
    self.practice = self.X_open_train
    self.X_open_train = np.array(self.X_open_train)
    self.y_open_train = np.array(self.y_open_train)
    self.X_open_test = np.array(self.X_open_test)
    self.y_open_test = np.array(self.y_open_test)




################################CLOSE############################################

    for i in range(len(self.close_df_train) - size):
      self.X_close_train.append(self.close_df_train[i : i + size])
      self.y_close_train.append(self.close_df_train[i + size])

    for i in range(len(self.close_df_test) - size):
      self.X_close_test.append(self.close_df_test[i : i + size])
      self.y_close_test.append(self.close_df_test[i + size])

    self.X_close_train = np.array(self.X_close_train)
    self.y_close_train = np.array(self.y_close_train)
    self.X_close_test = np.array(self.X_close_test)
    self.y_close_test = np.array(self.y_close_test)

    return 0
  
  def recurrent_nn(self, size, activations, learn_rate, iteration):
    model = keras.Sequential()
    model.add(keras.layers.LSTM(size, activation = activations, input_shape=(size, 1)))
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=learn_rate), loss="mse")
    model.add(Dense(units=1, activation = activations))

    history = model.fit(self.X_open_train, self.y_open_train, epochs = iteration)
    train_accuracy = model.fit(self.X_open_train, self.y_open_train)
    train_accuracy = model.evaluate(self.X_open_train, self.y_open_train)
    self.loss = history.history['loss']
    print("train loss", self.loss)

    self.y_train_predict = model.predict(self.X_open_train)
    train_mse = mean_squared_error(self.y_open_train, self.y_train_predict)
    print("train MSE", train_mse)

    y_test_predict = model.predict(self.X_open_test)
    test_mse = mean_squared_error(self.y_open_test, y_test_predict)
    print("test MSE", test_mse)

    
  def show(self):
    plt.plot(self.open_df_train)
    plt.plot(self.y_train_predict)
    #plt.plot(self.loss)
    plt.show()

if __name__ == "__main__":
    size = 5
    activation = 'tanh'
    learn_rate = 0.01
    iteration = 1000
    split_size = 0.8
    rnn = RNN("https://raw.githubusercontent.com/rlagkdms4372/cs4375/main/samsung_eletronics.csv") # put in path to your file
    rnn.preprocess(size,  split_size)
    rnn.recurrent_nn(size, activation, learn_rate, iteration)
    rnn.show()