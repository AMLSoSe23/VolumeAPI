import numpy as np
import cv2
import tensorflow as tf
import uvicorn

from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from tensorflow.keras.models import load_model
from keras.models import Model, model_from_json

from food_volume_estimation.volume_estimator import VolumeEstimator
from food_volume_estimation.depth_estimation.custom_modules import *
from food_volume_estimation.food_segmentation.food_segmentator import FoodSegmentator


app = FastAPI()
estimator = None

class EstimationData(BaseModel):
    img: List[int]
    plate_diameter: float

def load_volume_estimator(depth_model_architecture, depth_model_weights,
        segmentation_model_weights):
    """Loads volume estimator object and sets up its parameters."""
    # Create estimator object and intialize
    global estimator
    estimator = VolumeEstimator(arg_init=False)
    with open(depth_model_architecture, 'r') as read_file:
        custom_losses = Losses()
        objs = {'ProjectionLayer': ProjectionLayer,
                'ReflectionPadding2D': ReflectionPadding2D,
                'InverseDepthNormalization': InverseDepthNormalization,
                'AugmentationLayer': AugmentationLayer,
                'compute_source_loss': custom_losses.compute_source_loss}
        model_architecture_json = json.load(read_file)
        estimator.monovideo = model_from_json(model_architecture_json, custom_objects=objs)
    
    #----------------------------------------------
    depth_net = estimator.monovideo.get_layer('depth_net')
    estimator.depth_model = Model(inputs=depth_net.inputs,
                                  outputs=depth_net.outputs,
                                  name='depth_model')
    estimator.depth_model.load_weights(depth_model_weights)
    estimator.model_input_shape = (estimator.monovideo.inputs[0].shape.as_list()[1:])
    print('[*] Loaded depth estimation model.')
    # estimator.depth_model = load_model(depth_model_weights, custom_objects=objs)
    # estimator.model_input_shape = (estimator.monovideo.inputs[0].shape.as_list()[1:])
    # print('[*] Loaded depth estimation model.')

    # Depth model configuration
    MIN_DEPTH = 0.01
    MAX_DEPTH = 10
    estimator.min_disp = 1 / MAX_DEPTH
    estimator.max_disp = 1 / MIN_DEPTH
    estimator.gt_depth_scale = 0.35 # Ground truth expected median depth

    # Create segmentator object
    estimator.segmentator = FoodSegmentator(segmentation_model_weights)
    # Set plate adjustment relaxation parameter
    estimator.relax_param = 0.01

@app.post("/predict")
async def volume_estimation(data: EstimationData):
    img_byte_string = ' '.join([str(x) for x in data.img])
    np_img = np.fromstring(img_byte_string, np.int8, sep=' ')
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    volumes = estimator.estimate_volume(img, fov=70, plate_diameter_prior=data.plate_diameter, plots_directory='assets/output/')
    volumes = [v[0] * 1e6 for v in volumes]

    return {"volume": volumes}


if __name__ == '__main__':
    depth_model_architecture = 'models/depth_architecture.json'
    depth_model_weights = 'models/depth_extract.h5'
    segmentation_model_weights = 'models/segmentation_weights.h5'

    load_volume_estimator(depth_model_architecture,
                          depth_model_weights, 
                          segmentation_model_weights)
    
    uvicorn.run(app, host='0.0.0.0', port=5000)

