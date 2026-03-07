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
        print("\n--- DEBUG START ---")
        print(f"Type of self.image initially: {type(self.image)}")

        # 1. Retrieve the frame
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)

        print(f"Type of img returned by get_frame: {type(img)}")

        # Check if it has a 'value' attribute
        if hasattr(img, 'value'):
            print(f"Type of img.value: {type(img.value)}")
        else:
            print("img object does NOT have a 'value' attribute!")

        print("--- DEBUG END ---\n")

        # Returning the image exactly as it is so the node completes without crashing
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        qmodifier_model = build_response(context=self)
        return qmodifier_model

if "__main__" == __name__:
    Executor(sys.argv[1]).run()