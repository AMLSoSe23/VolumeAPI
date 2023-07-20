FROM python:3.10

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
      libgl1-mesa-glx \
      && rm -rf /var/lib/apt/lists/*

COPY food_volume_estimation/ food_volume_estimation/
COPY setup.py .
RUN python setup.py install

COPY food_volume_estimation_app.py .
COPY models/ models/

EXPOSE 5000

CMD ["python", "food_volume_estimation_app.py"]