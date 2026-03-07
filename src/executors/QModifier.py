"""
    QModifier component that modifies the Q value of an input image.
"""

import os
import sys



sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.QModifier.src.utils.response import build_response
from components.QModifier.src.models.PackageModel import PackageModel

import cv2
import numpy as np

class QModifier(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.q_value = self.request.get_param("QValue")
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # Retrieve the image frame from the database
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)

        #Define the encoding parameters for OpenCV
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.q_value]

        # Encode the image into memory using the JPEG format and the quality parameter
        success, encoded_img = cv2.imencode('.jpg', img, encode_param)

        if success:
            # Decode the image back to a standard frame format
            # This ensures the compression artifacts are applied before it moves to the next node
            img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        # Save the frame back
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)

        # Build and return the response model
        qmodifier_model = build_response(context=self)
        return qmodifier_model

if "__main__" == __name__:
    Executor(sys.argv[1]).run()