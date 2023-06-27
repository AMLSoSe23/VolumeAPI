FROM python:3.6

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall -y h5py
RUN pip install h5py==2.10.0
RUN pip install xlrd==1.2.0

# Install food-volume-estimation package
ADD food_volume_estimation/ food_volume_estimation/
copy setup.py .
RUN python setup.py install

# Add model files to image
COPY models/monovideo_fine_tune_food_videos.json models/depth_architecture.json
COPY models/monovideo_fine_tune_food_videos.h5 models/depth_weights.h5
COPY models/mask_rcnn_food_segmentation.h5 models/segmentation_weights.h5
COPY database/density_database.xlsx database/density_database.xlsx

# Copy and execute server script
COPY food_volume_estimation_app.py .
ENTRYPOINT ["python", "food_volume_estimation_app.py", \
            "--depth_model_architecture", "models/depth_architecture.json", \
            "--depth_model_weights", "models/depth_weights.h5", \
            "--segmentation_model_weights", "models/segmentation_weights.h5", \
            "--density_db_source", "database/density_database.xlsx"]

