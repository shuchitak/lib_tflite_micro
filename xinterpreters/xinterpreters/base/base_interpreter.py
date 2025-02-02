# Copyright 2022 XMOS LIMITED. This Software is subject to the terms of the
# XMOS Public License: Version 1
from abc import ABC, abstractmethod

from tflite import opcode2name
from tflite.Model import Model
from tflite.TensorType import TensorType


class xcore_tflm_base_interpreter(ABC):
    """! The xcore interpreters base class.
    Defines a common base interface to be used by the host and device interpreters.
    """

    def __init__(self) -> None:
        """! Base interpreter initializer.
        Initialises the list of models attached to the interpreter.
        """
        self.models = []
        return

    @abstractmethod
    def initialise_interpreter(self, model_index=0) -> None:
        """! Abstract meothd initialising an interpreter with the model  that has model_index.
        @param model_index  The model to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        """
        return

    @abstractmethod
    def set_input_tensor(self, data, input_index=0, model_index=0) -> None:
        """! Abstract method for writing the input tensor of a model.
        @param data  The blob of data to set the tensor to.
        @param input_index  The index of input tensor to target. Defaults to 0.
        @param model_index  The model to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        """
        return

    @abstractmethod
    def get_output_tensor(
        self, output_index=0, model_index=0, tensor=None
    ) -> "Output tensor data":
        """! Abstract method for reading data from the output tensor of a model.
        @param output_index  The index of output tensor to target.
        @param model_index  The model to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        @param tensor  Tensor of correct shape to write into (optional).
        @return  The data that was stored in the output tensor.
        """
        return

    @abstractmethod
    def get_input_tensor(self, input_index=0, model_index=0) -> "Input tensor data":
        """! Abstract for reading the data in the input tensor of a model.
        @param input_index  The index of input tensor to target.
        @param tensor Tensor of correct shape to write into (optional).
        @param model_index The engine to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        @return The data that was stored in the output tensor.
        """
        return

    @abstractmethod
    def invoke(self) -> None:
        """! Abstract method for invoking the model and starting inference of the current
        state of the tensors.
        """
        return

    @abstractmethod
    def close(self, model_index=0) -> None:
        """! Abstract method deleting the interpreter.
        @params model_index Defines which interpreter to target in systems with multiple.
        """
        return

    @abstractmethod
    def tensor_arena_size(self) -> "Size of tensor arena":
        """! Abstract method to read the size of the tensor arena required.
        @return size of the tensor arena as an integer.
        """
        return

    @abstractmethod
    def _check_status(self, status):
        """! Abstract method to read a status code and raise an exception.
        @param status Status code.
        """
        return

    @abstractmethod
    def print_memory_plan(self) -> None:
        """! Abstract method to print a plan of memory allocation"""
        return

    def get_input_tensor_size(
        self, input_index=0, model_index=0
    ) -> "Size of input tensor":
        """! Read the size of the input tensor from the model.
        @param input_index  The index of input tensor to target.
        @param model_index The model to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        @return The size of the input tensor as an integer.
        """

        # Select correct model from model list
        modelBuf = None
        for model in self.models:
            if model.tile == model_index:
                modelBuf = Model.GetRootAsModel(model.model_content, 0)
        # Get index of specific input tensor
        tensorIndex = modelBuf.Subgraphs(0).Inputs(input_index)

        tensorType = modelBuf.Subgraphs(0).Tensors(tensorIndex).Type()
        if tensorType == TensorType.INT8:
            tensorSize = 1  # int8 is 1 byte
        elif tensorType == TensorType.INT32:
            tensorSize = 4  # int32 is 4 bytes
        else:
            self._check_status(1)

        # Calculate tensor size by multiplying shape elements
        tensorSize = 1
        for i in range(0, modelBuf.Subgraphs(0).Tensors(tensorIndex).ShapeLength()):
            tensorSize = tensorSize * modelBuf.Subgraphs(0).Tensors(tensorIndex).Shape(
                i
            )
        return tensorSize

    def get_output_tensor_size(
        self, output_index=0, model_index=0
    ) -> "Size of output tensor":
        """! Read the size of the output tensor from the model.
        @param output_index  The index of output tensor to target.
        @param model_index The model to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        @return The size of the output tensor as an integer.
        """

        # Select correct model from model list
        modelBuf = None
        for model in self.models:
            if model.tile == model_index:
                modelBuf = Model.GetRootAsModel(model.model_content, 0)

        # Get index of specific output tensor
        tensorIndex = modelBuf.Subgraphs(0).Outputs(output_index)

        tensorType = modelBuf.Subgraphs(0).Tensors(tensorIndex).Type()
        if tensorType == TensorType.INT8:
            tensorSize = 1  # int8 is 1 byte
        elif tensorType == TensorType.INT32:
            tensorSize = 4  # int32 is 4 bytes
        else:
            self._check_status(1)

        # Calculate tensor size by multiplying shape elements
        for i in range(0, modelBuf.Subgraphs(0).Tensors(tensorIndex).ShapeLength()):
            tensorSize = tensorSize * modelBuf.Subgraphs(0).Tensors(tensorIndex).Shape(
                i
            )
        return tensorSize

    def get_input_details(
        self, input_index=0, model_index=0
    ) -> "Details of input tensor":
        """! Reads the input tensor details from the model.
        @param input_index  The index of input tensor to target.
        @param model_index The model to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        @return Tensor details, including the index, name, shape, data type, and quantization
        parameters.
        """

        # Select correct model from model list
        modelBuf = None
        for model in self.models:
            if model.tile == model_index:
                modelBuf = Model.GetRootAsModel(model.model_content, 0)

        tensorIndex = modelBuf.Subgraphs(0).Inputs(input_index)

        # Generate dictioary of tensor details
        if modelBuf.Subgraphs(0).Tensors(tensorIndex).Type() == TensorType.INT8:
            dtype = "int8"
        elif modelBuf.Subgraphs(0).Tensors(tensorIndex).Type() == TensorType.INT32:
            dtype = "int32"

        details = {
            "index": tensorIndex,
            "name": str(modelBuf.Subgraphs(0).Tensors(tensorIndex).Name())[1:].strip(
                "'"
            ),
            "shape": modelBuf.Subgraphs(0).Tensors(tensorIndex).ShapeAsNumpy(),
            "dtype": dtype,
            "quantization": (
                modelBuf.Subgraphs(0).Tensors(tensorIndex).Quantization().Scale(0),
                modelBuf.Subgraphs(0).Tensors(0).Quantization().ZeroPoint(0),
            ),
        }

        return details

    def get_output_details(
        self, output_index=0, model_index=0
    ) -> "Details of output tensor":
        """! Reads the output tensor details from the model.
        @param output_index  The index of output tensor to target.
        @param model_index The model to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        @return Tensor details, including the index, name, shape, data type, and quantization
        parameters.
        """

        # Select correct model from models list
        modelBuf = None
        for model in self.models:
            if model.tile == model_index:
                modelBuf = Model.GetRootAsModel(model.model_content, 0)

        # Output tensor is last tensor
        tensorIndex = modelBuf.Subgraphs(0).Outputs(output_index)

        # Generate dictioary of tensor details
        if modelBuf.Subgraphs(0).Tensors(tensorIndex).Type() == TensorType.INT8:
            dtype = "int8"
        elif modelBuf.Subgraphs(0).Tensors(tensorIndex).Type() == TensorType.INT32:
            dtype = "int32"

        details = {
            "index": tensorIndex,
            "name": str(modelBuf.Subgraphs(0).Tensors(tensorIndex).Name())[1:].strip(
                "'"
            ),
            "shape": modelBuf.Subgraphs(0).Tensors(tensorIndex).ShapeAsNumpy(),
            "dtype": dtype,
            "quantization": (
                modelBuf.Subgraphs(0).Tensors(tensorIndex).Quantization().Scale(0),
                modelBuf.Subgraphs(0).Tensors(tensorIndex).Quantization().ZeroPoint(0),
            ),
        }

        return details

    def set_model(
        self,
        model_path=None,
        model_content=None,
        params_path=None,
        params_content=None,
        model_index=0,
    ) -> None:
        """! Adds a model to the interpreter's list of models.
        @param model_path The path to the model file (.tflite), alternative to model_content.
        @param model_content The byte array representing a model, alternative to model_path.
        @param params_path The path to the params file for the model,
        alternative to params_content (optional).
        @param params_content The byte array representing the model parameters,
        alternative to params_path (optional).
        @param model_index The modell to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        """

        # Check model_path or model_content is valid
        if type(model_path) == str or model_content is not None:
            tile_found = False
            # Find correct model and replace
            for model in self.models:
                if model.tile == model_index:
                    model = self.modelData(
                        model_path,
                        model_content,
                        params_path,
                        params_content,
                        model_index,
                    )
                    tile_found = True
                    break
            # If model wasn't previously set, add it to list
            if not tile_found:
                self.models.append(
                    self.modelData(
                        model_path,
                        model_content,
                        params_path,
                        params_content,
                        model_index,
                    )
                )
            self.initialise_interpreter(model_index)

    class modelData:
        """! The model data class
        A class that holds a model and data associated with a single model.
        """

        def __init__(
            self, model_path, model_content, params_path, params_content, model_index
        ):
            """! Model data initializer.
            Sets up variables, generates a list of operators used in the model,
            and reads model and params paths into byte arrays (content).
            @param model_path Path to the model file (.tflite).
            @param model_content Model model_content (byte array).
            @param params_path Path to model parameters file.
            @param params_content Model parameters content (byte array)
            @param model_index The model to target, for interpreters that support multiple models
            running concurrently. Defaults to 0 for use with a single model.
            """
            self.model_path = model_path
            self.model_content = model_content
            self.params_path = params_path
            self.params_content = params_content
            self.tile = model_index
            self.opList = []
            self.pathToContent()
            self.modelToOpList()

        def modelToOpList(self):
            """! Generates operator list from model."""

            # Load model
            buffer = self.model_content
            model = Model.GetRootAsModel(buffer, 0)
            self.opList = []

            # Iterate through operators in model and add operators to opList
            for y in range(0, model.Subgraphs(0).OperatorsLength()):
                opcode = model.OperatorCodes(
                    model.Subgraphs(0).Operators(y).OpcodeIndex()
                )
                # If custom opcode parse string
                if opcode.BuiltinCode() == 32:
                    self.opList.append(str(opcode.CustomCode()).strip("b'"))
                # If built in op code, decode
                else:
                    self.opList.append(opcode2name(opcode.BuiltinCode()))

        def pathToContent(self):
            """! Reads model and params paths to content (byte arrays)"""

            # Check if path exists but not content
            if self.model_content == None and self.model_path != None:
                with open(self.model_path, "rb") as input_fd:
                    self.model_content = input_fd.read()

            # Check if params_path exits but not params_content
            if self.params_content == None and self.params_path != None:
                with open(self.params_path, "rb") as input_fd2:
                    self.params_content = input_fd2.read()
            # If no params, set to empty byte array
            else:
                self.params_content = bytes([])
