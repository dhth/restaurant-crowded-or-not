FROM python:3.6-slim-stretch

RUN apt update
RUN apt install -y python3-dev gcc wget

# Install pytorch and fastai
RUN pip install torch_nightly -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html
RUN pip install fastai

# Install starlette and uvicorn
RUN pip install starlette uvicorn python-multipart aiohttp

ADD run.py run.py

RUN wget https://storage.googleapis.com/dhruvs-saved-models/saved_models/restaurant-crowded-or-not/rest-saved-model1.pth && mkdir -p data/models && mv rest-saved-model1.pth data/models/

EXPOSE 8008

# Start the server
CMD ["python", "run.py", "serve"]
