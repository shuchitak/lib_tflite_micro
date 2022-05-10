# Copyright 2022 XMOS LIMITED. This Software is subject to the terms of the
# XMOS Public License: Version 1
import struct
import array
import numpy as np
from abc import abstractmethod

from xinterpreters.base.base_interpreter import xcore_tflm_base_interpreter
import xinterpreters.device.aisrv_cmd as aisrv_cmd

XCORE_IE_MAX_BLOCK_SIZE = 512 

class AISRVError(Exception):
    """Error from device"""
    pass

class IOError(AISRVError):
    """IO Error from device"""
    pass

class NoModelError(AISRVError):
    """No model error from device"""
    pass

class ModelError(AISRVError):
    """Model error from device"""
    pass

class InferenceError(AISRVError):
    """Inference Error from device"""
    pass

class CommandError(AISRVError):
    """Command Error from device"""
    pass

class xcore_tflm_device_interpreter(xcore_tflm_base_interpreter):

    def __init__(self):
        self._timings_length = None
        self._max_block_size = XCORE_IE_MAX_BLOCK_SIZE # TODO read from (usb) device?
        self._spec_length = 20 # TODO fix magic number

        super().__init__()

    def initialise_interpreter(self, model_index=0) -> None:
        """! Abstract initialising interpreter with model associated with model_index.
        @param model_index The engine to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        """
        currentModel = None
        for model in self.models:
            if model.tile == model_index:
                currentModel = model

        self.connect()
        self.download_model(
            bytearray(currentModel.model_content),
            currentModel.secondary_memory,
            currentModel.flash,
            currentModel.tile
            )
        return

    def set_input_tensor(self, input_index, data, model_index=0) -> None:
        """! Abstract for writing the input tensor of a model.
        @param input_index  The index of input tensor to target.
        @param data  The blob of data to set the tensor to.
        @param model_index The engine to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        """
        self._download_data(aisrv_cmd.CMD_SET_INPUT_TENSOR, data, tensor_num = input_index, engine_num = model_index)
        return

    def get_output_tensor(self, output_index=0, tensor=None, model_index=0) -> "Output tensor data":
        """! Abstract for reading the data in the output tensor of a model.
        @param output_index  The index of output tensor to target.
        @param tensor Tensor of correct shape to write into (optional)
        @param model_index The engine to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        @return The data that was stored in the output tensor.
        """
        output_length = self.get_output_tensor_size(output_index, model_index)
        data_read = self._upload_data(aisrv_cmd.CMD_GET_OUTPUT_TENSOR, output_length, tensor_num = output_index, engine_num = model_index)

        assert type(data_read) == list
        assert type(data_read[0]) == int

        return self.bytes_to_ints(data_read)

    def get_input_tensor(self, input_index=0, model_index=0) -> "Input tensor data":
        """! Abstract for reading the data in the input tensor of a model.
        @param output_index  The index of output tensor to target.
        @param tensor Tensor of correct shape to write into (optional)
        @param model_index The engine to target, for interpreters that support multiple models
        running concurrently. Defaults to 0 for use with a single model.
        @return The data that was stored in the output tensor.
        """
        # Retrieve result from device
        input_length = self.get_input_tensor_size(input_index, model_index)
        data_read = self._upload_data(aisrv_cmd.CMD_GET_INPUT_TENSOR, input_length, tensor_num = input_index, engine_num = model_index)

        assert type(data_read) == list
        assert type(data_read[0]) == int

        return self.bytes_to_ints(data_read)

    @abstractmethod
    def invoke(self) -> None:
        pass

    def close(self, model_index=0) -> None:
        """! Abstract deleting the interpreter
        @params model_index Defines which interpreter to target in systems with multiple
        """
        return  

    def tensor_arena_size(self) -> "Size of tensor arena":
        """! Abstract to read the size of the tensor arena required
        @return size of the tensor arena as an integer
        """
        return

    def _check_status(self, status):
        """! Abstract to read a status code and raise an exception
        @param status Status code
        """
        return

    def print_memory_plan(self) -> None:
        """! Abstract to print a plan of memory allocation
        """
        return

    #Internal Device Interpreter Functions

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def _clear_error(self):
        pass

    def download_model(self, model_bytes, secondary_memory = False, flash = False, engine_num = 0):
        
        if not flash:
            assert type(model_bytes) == bytearray
            
            print("Model length (bytes): " + str(len(model_bytes)))
           

            if secondary_memory:
                print("Downloading model to secondary memory")
                cmd = aisrv_cmd.CMD_SET_MODEL_SECONDARY
            else:
                print("Downloading model to primary memory")
                cmd = aisrv_cmd.CMD_SET_MODEL_PRIMARY

        elif flash:
            if secondary_memory:
                print("Loading model to secondary memory")
                cmd = aisrv_cmd.CMD_SET_MODEL_SECONDARY_FLASH
            else:
                print("Loading model to primary memory")
                cmd = aisrv_cmd.CMD_SET_MODEL_PRIMARY_FLASH


        try:
            # Download model to device
            self._download_data(cmd, model_bytes, engine_num = engine_num)
        except IOError:
            self._clear_error()
            raise IOError

    def bytes_to_ints(self, data_bytes, bpi=1):

        output_data_int = []

        # TODO better way of doing this?
        for i in range(0, len(data_bytes), bpi):
            x = data_bytes[i:i+bpi]
            y =  int.from_bytes(x, byteorder = "little", signed=True)
            output_data_int.append(y)

        return output_data_int

    def read_debug_log(self):

        debug_string = self._upload_data(aisrv_cmd.CMD_GET_DEBUG_LOG, 300) #TODO rm magic number

        r = bytearray(debug_string).decode('utf8', errors='replace')
        return r

    def read_times(self, model_index = 0):
        for model in self.models:
            if model.tile == model_index:
                ops_length = len(model.opList)
        times_bytes = self._upload_data(aisrv_cmd.CMD_GET_TIMINGS, ops_length*4, engine_num = model_index)
        times_ints = self.bytes_to_ints(times_bytes, bpi=4)
        return times_ints

class xcore_tflm_spi_interpreter(xcore_tflm_device_interpreter):
    def __init__(self, bus=0, device=0, speed=7800000):
        self._dev = None
        self._bus = bus
        self._device = device
        self._speed = speed
        self._dummy_bytes = [0,0,0] # cmd + 2 dummy
        self._dummy_byte_count = len(self._dummy_bytes)
        super().__init__()

    def _download_data(self, cmd, data_bytes):
        
        data_len = len(data_bytes)
        
        data_index = 0

        data_ints = self.bytes_to_ints(data_bytes)
        
        while data_len >= self._max_block_size:
            
            self._wait_for_device()

            to_send = [cmd]
            to_send.extend(data_ints[data_index:data_index+self._max_block_size])

            data_len = data_len - self._max_block_size
            data_index = data_index  + self._max_block_size

            self._dev.xfer(to_send)
        
        # Note, send a 0 length if size % XCORE_IE_MAX_BLOCK_SIZE == 0
        status = self._wait_for_device()
        to_send = [cmd]
        to_send.extend(data_ints[data_index:data_index+data_len])
        self._dev.xfer(to_send)

    def _upload_data(self, cmd, length):

        self._wait_for_device()

        to_send = self._construct_packet(cmd, length+1)
    
        r = self._dev.xfer(to_send)

        #r = [x-256 if x > 127 else x for x in r]
        r = r[self._dummy_byte_count:]
        return r[:length]
  
    def _clear_error(self):
        """Clear error bits in status register"""
        # Error flags are cleared by GET_STATUS
        pass       

    def connect(self):
        import spidev
        self._dev = spidev.SpiDev()
        self._dev.open(self._bus, self._device)
        self._dev.max_speed_hz = self._speed

    # TODO move to super()
    def start_inference(self):

        to_send = self._construct_packet(aisrv_cmd.CMD_START_INFER, 0)
        r =  self._dev.xfer(to_send)

    def _construct_packet(self, cmd, length):

        def round_to_word(x):
            return 4 * round(x/4)

        return [cmd] + self._dummy_bytes + (round_to_word(length) * [0])

   
    def _read_status(self):

        to_send = [aisrv_cmd.CMD_GET_STATUS] + self._dummy_bytes + (4 * [0])
        r =  self._dev.xfer(to_send)

        return r[self._dummy_byte_count] # TODO more than 1 status byte?

    def _wait_for_device(self):
        """Wait for device to report not busy. Raise exception on any error Status"""
        
        while True:
            
            status = self._read_status()
           
            if status != 1: #TODO STATUS_BUSY

                if status == 0x04: # TODO STATUS_ERROR_NO_MODEL
                    raise NoModel()
                elif status == 0x08: # TODO STATUS_ERROR_MODEL_ERR
                    raise ModelError()
                elif status == 0x10: # TODO STATUS_ERROR_INFER_ERR
                    raise InferenceError()
                elif status == 0x20: # TODO STATUS_BAD_CMD
                    raise CommandError()

                break;

class xcore_tflm_usb_interpreter(xcore_tflm_device_interpreter):
    def __init__(self, timeout = 500000):
        self._out_ep = None
        self._in_ep = None
        self._dev = None
        self._timeout = timeout
        super().__init__()

    def _download_data(self, cmd, data_bytes, tensor_num = 0, engine_num = 0):
        import usb
        
        try:
            self._out_ep.write(bytes([cmd, engine_num, tensor_num]))

            self._out_ep.write(data_bytes, 1000)

            if (len(data_bytes) % self._max_block_size) == 0:
                self._out_ep.write(bytearray([]), 1000)

        except usb.core.USBError as e:
            if e.backend_error_code == usb.backend.libusb1.LIBUSB_ERROR_PIPE:
                #print("USB error, IN/OUT pipe halted")
                raise IOError()
   
    def _upload_data(self, cmd, length, sign = False, tensor_num = 0, engine_num = 0):
        import usb
        read_data = []

        try:  
            self._out_ep.write(bytes([cmd, engine_num, tensor_num]), self._timeout)
            buff = usb.util.create_buffer(self._max_block_size)
        
            while True:

                read_len = self._dev.read(self._in_ep, buff, 10000)

                read_data.extend(buff[:read_len])

                if read_len != self._max_block_size:
                    break;

            return read_data
        
        except usb.core.USBError as e:
            if e.backend_error_code == usb.backend.libusb1.LIBUSB_ERROR_PIPE:
                #print("USB error, IN/OUT pipe halted")
                raise IOError()

    def _clear_error(self):
        self._dev.clear_halt(self._out_ep)
        self._dev.clear_halt(self._in_ep)

    def connect(self):

        import usb
        self._dev = None
        while self._dev is None:

            # TODO - more checks that we have the right device..
            self._dev = usb.core.find(idVendor=0x20b1, idProduct=0xa15e)

            # set the active configuration. With no arguments, the first
            # configuration will be the active one
            self._dev.set_configuration()

            # get an endpoint instance
            cfg = self._dev.get_active_configuration()

            #print("found device: \n" + str(cfg))
            intf = cfg[(0,0)]

            self._out_ep = usb.util.find_descriptor(
                intf,
                # match the first OUT endpoint
                custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT)

            self._in_ep = usb.util.find_descriptor(
                intf,
                # match the first IN endpoint
                custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_IN)

            assert self._out_ep is not None
            assert self._in_ep is not None

            print("Connected to AISRV via USB")

    def invoke(self):
        # Send cmd
        print("Inferencing...")
        engine_num=0
        self._out_ep.write(bytes([aisrv_cmd.CMD_START_INFER, engine_num, 0]), 1000)

        # Send out a 0 length packet 
        self._out_ep.write(bytes([]), 1000)

    # TODO move to super()
    def start_acquire_single(self, sx, ex, sy, ey, rw, rh, engine_num = 0):

        # Send cmd
        self._out_ep.write(bytes([aisrv_cmd.CMD_START_ACQUIRE_SINGLE, engine_num, 0]), 1000)
        def tobytes(l):
            o = []
            for i in l:
                o.append( i & 0xff )
                o.append( (i>>8) & 0xff )
            return bytes(o)
        # Send out packet with coordinates 
        self._out_ep.write(tobytes([sx, ex, sy, ey, rw, rh]), 1000)

    def acquire_set_i2c(self, i2c_address, reg_address, reg_value, engine_num = 0):

        # Send cmd
        self._out_ep.write(bytes([aisrv_cmd.CMD_START_ACQUIRE_SET_I2C, engine_num, 0]), 1000)
        def tobytes(l):
            o = []
            for i in l:
                o.append( i & 0xff )
            return bytes(o)
        # Send out packet with coordinates 
        self._out_ep.write(tobytes([i2c_address, reg_address, reg_value]), 1000)

    # TODO move to super()
    def start_acquire_stream(self, engine_num = 0):

        # Send cmd
        self._out_ep.write(bytes([aisrv_cmd.CMD_START_ACQUIRE_STREAM, engine_num, 0]), 1000)

        # Send out a 0 length packet 
        self._out_ep.write(bytes([]), 1000)

    #TODO move to super()
    def enable_output_gpio(self, engine_num = 0):

        self._out_ep.write(bytes([aisrv_cmd.CMD_SET_OUTPUT_GPIO_EN, engine_num, 0]), 1000)
        self._out_ep.write(bytes([1]), 1000)
    
    #TODO move to super()
    def disable_output_gpio(self, engine_num = 0):

        self._out_ep.write(bytes([aisrv_cmd.CMD_SET_OUTPUT_GPIO_EN, engine_num, 0]), 1000)
        self._out_ep.write(bytes([0]), 1000)

    def set_output_gpio_threshold(self, index, threshold):
        
        self._out_ep.write(bytes([aisrv_cmd.CMD_SET_OUTPUT_GPIO_THRESH, engine_num, 0]), 1000)
        self._out_ep.write(bytes([index, threshold]), 1000)

    def set_output_gpio_mode_max(self, engine_num = 0):
        
        self._out_ep.write(bytes([aisrv_cmd.CMD_SET_OUTPUT_GPIO_MODE, engine_num, 0]), 1000)
        self._out_ep.write(bytes([1]), 1000)

    def set_output_gpio_mode_none(self, engine_num = 0):
        
        self._out_ep.write(bytes([aisrv_cmd.CMD_SET_OUTPUT_GPIO_MODE, engine_num, 0]), 1000)
        self._out_ep.write(bytes([0]), 1000)