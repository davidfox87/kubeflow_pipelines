import argparse
from datetime import datetime
import tensorflow as tf

parser = argparse.ArgumentParser()
parser.add_argument(
    '--model_file', type=str, required=True, help='Name of the model file.')
parser.add_argument(
    '--bucket', type=str, required=True, help='S3 bucket name.')
args = parser.parse_args()

bucket=args.bucket
model_file=args.model_file

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(512, activation=tf.nn.relu),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print(model.summary())    

mnist = tf.keras.datasets.mnist
(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

callbacks = [
  tf.keras.callbacks.TensorBoard(log_dir=bucket + '/logs/' + datetime.now().date().__str__()),
  # Interrupt training if val_loss stops improving for over 2 epochs
  tf.keras.callbacks.EarlyStopping(patience=2, monitor='val_loss'),
]

model.fit(x_train, y_train, batch_size=32, epochs=5, callbacks=callbacks,
          validation_data=(x_test, y_test))


model.save(model_file)

from tensorflow import gfile

s3_path = bucket + "/" + model_file

if gfile.Exists(s3_path):
    gfile.Remove(s3_path)

gfile.Copy(model_file, s3_path)
with open('/output.txt', 'w') as f:
  f.write(s3_path)