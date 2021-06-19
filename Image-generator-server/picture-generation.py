from deep_daze import Imagine
import sys
import base64
from PIL import Image
from io import BytesIO
import requests

TEXT = sys.argv[1]
NUM_LAYERS = 32
IMAGE_WIDTH = 128
SAVE_PROGRESS = True
LEARNING_RATE = 1e-5
ITERATIONS = 200
SAVE_EVERY = ITERATIONS
EPOCHS = 10

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
filenameData = filename + ".jpg"

#with open("getArgu.txt", 'w') as f:
#    f.write("text " + sys.argv[1] + "\nstoryboard " + sys.argv[2] + "\ncase " + sys.argv[3] + "\nowner_id " + sys.argv[4])

for epoch in range(EPOCHS):
    for i in range(ITERATIONS):
        model.train_step(epoch, i)

        if i % model.save_every == 0:
            with open(filenameData, 'rb') as f:
                data = base64.b64encode(f.read())
                response = requests.post("http://192.168.1.16:8000/update_picture_by_flask/",
                                         data={"pictureB64": data, "storyboard_id": sys.argv[2], "case_id": sys.argv[3], "owner_id": sys.argv[4]})


                #with open("getData.txt", 'wb') as f:
                #    f.write(data)
                #img = Image.open(BytesIO(base64.b64decode(data)))
                #img.save("mabite.png", "PNG")