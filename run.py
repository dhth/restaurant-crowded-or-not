from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse

from fastai.vision import ImageDataBunch, create_cnn, open_image, get_transforms, imagenet_stats, models, show_image
from pathlib import Path

from io import BytesIO

import sys
import uvicorn
import aiohttp
import asyncio


async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


app = Starlette()

path = Path('data/')

classes = ['crowded', 'empty']
data2 = ImageDataBunch.single_from_classes(path, classes, tfms=get_transforms(), size=224).normalize(imagenet_stats)
learn = create_cnn(data2, models.resnet34)
learn.load('rest-saved-model1')

index_html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Restaurant:crowded-or-empty</title>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

  </head>

  <body class="bg-light">

    <div class="container">
      <div class="py-5 text-center">
        <h2>Restaurant: Crowded or Empty</h2>
        <p class="lead">This is an image classifier API that takes in an image of a restaurant interior and predicts if the restaurant is crowded or empty.</p>
      </div>
<div class="row justify-content-center">
    <div class="col-6">
      
      <form  action="/upload" method="post" enctype="multipart/form-data">
        <h4 class="mb-3">Select image to upload:</h4>
        <div class="form-group">
            <input type="file" name="file">
            <input type="submit" value="Upload Image">
        </div>
        </form>
      
      <br><br>
      <h4 class="mb-3">Or submit a URL::</h4>
        
        <form action="/classify-url" method="get">
            <input type="url" name="url">
            <input type="submit" value="Fetch and analyze image">
          </form
          

  </div>
        

      <footer class="my-5 pt-5 text-muted text-center text-small">
        <p class="mb-1">Made by <a target="_" href="https://github.com/dhth/">dhruv</a></p>
        <ul class="list-inline">
          <li class="list-inline-item"><a target="_" href="https://github.com/dhth/restaurant-crowded-or-not">source</a></li>
        </ul>
      </footer>
    </div>
    
  </body>
</html>
"""


resp_html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Restaurant:crowded-or-empty</title>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

  </head>

  <body class="bg-light">

    <div class="container">
      <div class="py-5 text-center">
        <h2>Restaurant: Crowded or Empty</h2>
        <br><br>
        <p class="lead">It appears to be <b>{}</b></p>
        <p class="lead"><a href="/">go back</a></p>
      </div>

<div class="row justify-content-center">
      <footer class="my-5 pt-5 text-muted text-center text-small">
        <p class="mb-1">Made by <a target="_" href="https://github.com/dhth/">dhruv</a></p>
        <ul class="list-inline">
          <li class="list-inline-item"><a target="_" href="https://github.com/dhth/restaurant-crowded-or-not">source</a></li>
        </ul>
      </footer>
    </div>
    </div>
  </body>
</html>
"""




@app.route("/upload", methods=["POST"])
async def upload(request):
    data = await request.form()
    bytes = await (data["file"].read())
    return predict_image_from_bytes(bytes)


@app.route("/classify-url", methods=["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    return predict_image_from_bytes(bytes)


def predict_image_from_bytes(bytes):
    img = open_image(BytesIO(bytes))
    pred_class,pred_idx,outputs = learn.predict(img)
    return HTMLResponse(resp_html.format(str(pred_class)))
    #return JSONResponse({
    #    "prediction": pred_class
    #})



@app.route("/")
def form(request):
    return HTMLResponse(index_html)


@app.route("/form")
def redirect_to_homepage(request):
    return RedirectResponse("/")


if __name__ == "__main__":
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8008)
