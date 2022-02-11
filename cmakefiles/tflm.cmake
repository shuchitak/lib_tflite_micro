set(TFLIB_SRC_DIR
  "${CMAKE_CURRENT_SOURCE_DIR}/../lib_tflite_micro/src/tflite-xcore-kernels")

set(TFLITE_SRC_DIR
  "${CMAKE_CURRENT_SOURCE_DIR}/../lib_tflite_micro/submodules/tflite-micro/tensorflow/lite")

set(TFLM_SRC_DIR
  "${TFLITE_SRC_DIR}/micro")

set(NN_SRC_DIR
  "${CMAKE_CURRENT_SOURCE_DIR}/../../lib_nn/lib_nn/src")

file(GLOB_RECURSE ALL_SOURCES "${NN_SRC_DIR}/c/*.c")

list(APPEND ALL_SOURCES  "${TFLITE_SRC_DIR}/c/common.c")

list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/AggregateFn.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/AggregateFn_DW.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/Filter2D.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/MaxPool2d.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/MaxPoolAgg.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/MemCpyFn.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/OutputTransformFn.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/filt2d/conv2d_utils.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/filt2d/util.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/filt2d/geom/Filter2dGeometry.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/filt2d/geom/ImageGeometry.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/filt2d/geom/WindowGeometry.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/cpp/filt2d/geom/WindowLocation.cpp")
list(APPEND ALL_SOURCES  "${NN_SRC_DIR}/asm/asm_constants.c")

list(APPEND ALL_SOURCES  "${TFLITE_SRC_DIR}/core/api/error_reporter.cc")
list(APPEND ALL_SOURCES  "${TFLITE_SRC_DIR}/core/api/tensor_utils.cc")
list(APPEND ALL_SOURCES  "${TFLITE_SRC_DIR}/core/api/flatbuffer_conversions.cc")
list(APPEND ALL_SOURCES  "${TFLITE_SRC_DIR}/core/api/op_resolver.cc")
list(APPEND ALL_SOURCES  "${TFLITE_SRC_DIR}/kernels/kernel_util.cc")
list(APPEND ALL_SOURCES  "${TFLITE_SRC_DIR}/kernels/internal/quantization_util.cc")
list(APPEND ALL_SOURCES  "${TFLITE_SRC_DIR}/schema/schema_utils.cc")

list(APPEND ALL_SOURCES  "${CMAKE_CURRENT_SOURCE_DIR}/../lib_tflite_micro/src/inference_engine.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_activations.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_add.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_arg_min_max.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_bconv2d.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_bsign.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_conv2d.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_conv2d_v2.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/strided_slice_v2.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_custom_options.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_detection_post.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_dispatcher.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_error_reporter.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_extended_interpreter.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_fully_connected.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_interpreter.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_load_from_flash.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_pad.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_planning.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_pooling.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_profiler.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_type_conversions.cc")
list(APPEND ALL_SOURCES  "${TFLIB_SRC_DIR}/xcore_utils.cc")

list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/all_ops_resolver.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/flatbuffer_utils.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/memory_helpers.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_allocator.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_error_reporter.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_graph.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_interpreter.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_profiler.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_string.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_time.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_utils.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/mock_micro_graph.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/recording_micro_allocator.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/recording_simple_memory_allocator.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/simple_memory_allocator.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/system_setup.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/all_ops_resolver.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/flatbuffer_utils.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/memory_helpers.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_allocator.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_error_reporter.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_graph.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_interpreter.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_profiler.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_resource_variable.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_string.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_time.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/micro_utils.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/mock_micro_graph.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/recording_micro_allocator.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/recording_simple_memory_allocator.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/simple_memory_allocator.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/system_setup.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/test_helpers.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/memory_planner/greedy_memory_planner.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/activations.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/activations_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/add.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/add_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/add_n.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/arg_min_max.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/assign_variable.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/batch_to_space_nd.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/call_once.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/cast.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/ceil.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/circular_buffer.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/circular_buffer_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/circular_buffer_flexbuffers_generated_data.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/comparisons.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/concatenation.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/conv.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/conv_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/cumsum.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/depth_to_space.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/depthwise_conv.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/depthwise_conv_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/dequantize.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/dequantize_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/detection_postprocess_flexbuffers_generated_data.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/elementwise.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/elu.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/ethosu.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/exp.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/expand_dims.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/fill.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/floor.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/floor_div.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/floor_mod.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/fully_connected.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/fully_connected_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/gather.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/gather_nd.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/hard_swish.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/hard_swish_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/if.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/kernel_runner.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/kernel_util.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/l2_pool_2d.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/l2norm.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/leaky_relu.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/leaky_relu_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/log_softmax.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/logical.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/logical_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/logistic.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/logistic_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/maximum_minimum.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/mul.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/mul_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/neg.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/pack.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/pad.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/pooling.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/pooling_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/prelu.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/prelu_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/quantize.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/quantize_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/read_variable.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/reduce.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/reshape.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/resize_bilinear.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/resize_nearest_neighbor.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/round.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/shape.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/softmax.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/softmax_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/space_to_batch_nd.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/space_to_depth.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/split.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/split_v.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/squeeze.cc")

list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/sub.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/sub_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/svdf.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/svdf_common.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/tanh.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/transpose.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/transpose_conv.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/unpack.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/var_handle.cc")
list(APPEND ALL_SOURCES  "${TFLM_SRC_DIR}/kernels/zeros_like.cc")

list(APPEND ALL_SOURCES  "${CMAKE_CURRENT_SOURCE_DIR}/../lib_tflite_micro/submodules/flatbuffers/src/util.cpp")

set(ALL_INCLUDES "")

list(APPEND ALL_INCLUDES  ${XCORE_INTERPRETER_INCLUDES})
list(APPEND ALL_INCLUDES  "${CMAKE_CURRENT_SOURCE_DIR}/src")
list(APPEND ALL_INCLUDES  "${CMAKE_CURRENT_SOURCE_DIR}/../lib_tflite_micro/api")
list(APPEND ALL_INCLUDES  "${CMAKE_CURRENT_SOURCE_DIR}/../lib_tflite_micro/src/tflite-xcore-kernels")
list(APPEND ALL_INCLUDES  "${CMAKE_CURRENT_SOURCE_DIR}/../lib_tflite_micro/submodules/tflite-micro")
list(APPEND ALL_INCLUDES  "${CMAKE_CURRENT_SOURCE_DIR}/../lib_tflite_micro/submodules/gemmlowp")
list(APPEND ALL_INCLUDES  "${CMAKE_CURRENT_SOURCE_DIR}/../lib_tflite_micro/submodules/ruy")
list(APPEND ALL_INCLUDES  "${CMAKE_CURRENT_SOURCE_DIR}/../lib_tflite_micro/submodules/flatbuffers/include")
list(APPEND ALL_INCLUDES  "${CMAKE_CURRENT_SOURCE_DIR}/../../lib_nn/")
list(APPEND ALL_INCLUDES  "${CMAKE_CURRENT_SOURCE_DIR}/../../lib_nn/lib_nn/api")
list(APPEND ALL_INCLUDES  "${XMOS_TOOL_PATH}/target/include/")
