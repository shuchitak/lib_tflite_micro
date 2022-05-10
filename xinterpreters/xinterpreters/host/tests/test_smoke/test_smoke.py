#!/usr/bin/env python
# Copyright (c) 2020, XMOS Ltd, All rights reserved

import sys, os
import numpy as np
import cv2

from xinterpreters import xcore_tflm_host_interpreter

ie = xcore_tflm_host_interpreter()
ie.set_model(model_path="./smoke_model.tflite", params_path="./smoke_model.flash")
with open("./detection_0.raw", "rb") as fd:
    img = fd.read()

ie.set_input_tensor(0, img)
ie.invoke()

answer1 = ie.get_output_tensor(0)
answer2 = ie.get_output_tensor(1)
with open("./out0", "wb") as fd:
    fd.write(answer1)
with open("./out1", "wb") as fd:
    fd.write(answer2)
