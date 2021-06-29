from deep_daze import Imagine
import sys
import base64
import requests
import os
import cv2
from cv2 import dnn_superres

TEXT = sys.argv[1]
NUM_LAYERS = 32
IMAGE_WIDTH = 64
SAVE_PROGRESS = True
LEARNING_RATE = 1e-5
ITERATIONS = 200
SAVE_EVERY = ITERATIONS
EPOCHS = 5
SR_MODEL = "edsr"

sr = dnn_superres.DnnSuperResImpl_create()
path = f"models/{SR_MODEL}_x4.pb"
sr.readModel(path)
sr.setModel(SR_MODEL, 4)

model = Imagine(
    text=TEXT,
    num_layers=NUM_LAYERS,
    save_every=SAVE_EVERY,
    image_width=IMAGE_WIDTH,
    lr=LEARNING_RATE,
    iterations=ITERATIONS,
    save_progress=SAVE_PROGRESS
)
filename = f"data/{sys.argv[2]}-{sys.argv[3]}-{sys.argv[4]}"
model.textpath = filename
image_filename = filename + ".jpg"
image_upscaled_fn = filename + "_upscaled.jpg"

for epoch in range(EPOCHS):
    for i in range(ITERATIONS):
        model.train_step(epoch, i)

        if epoch != 0 and i % model.save_every == 0:
            img = cv2.imread(image_filename)
            output = sr.upsample(img)
            cv2.imwrite(image_upscaled_fn, output)
            with open(image_upscaled_fn, 'rb') as f:
                data = base64.b64encode(f.read())
                response = requests.post("http://10.0.1.158:8000/update_picture_by_flask/",
                #response = requests.post("http://192.168.1.14:8000/update_picture_by_flask/",
                #response = requests.post("http://127.0.0.1:8000/update_picture_by_flask/",
                                         data={"pictureB64": data, "storyboard_id": sys.argv[2], "case_id": sys.argv[3], "owner_id": sys.argv[4]})

            try:
                os.remove(image_upscaled_fn)
                os.remove(filename + ".00000" + str(epoch) + ".jpg")
            except:
                print("Error")

try:
    os.remove(image_filename)
except:
    print("Error")
