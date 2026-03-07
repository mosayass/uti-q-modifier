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
        # Retrieve the image frame
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)

        # Safely convert QValue to integer to satisfy OpenCV requirements
        q_val_int = int(float(self.q_value))
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), q_val_int]

        # Encode and decode the image to apply the compression artifacts
        success, encoded_img = cv2.imencode('.jpg', img.value, encode_param)

        if success:
            img.value = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

        # Save the frame back to the database
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)

        # Build and return the response
        package_model = build_response(context=self)
        return package_model

if "__main__" == __name__:
    Executor(sys.argv[1]).run()