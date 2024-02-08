cmake_minimum_required(VERSION 3.10)
project(rvv-intrinsics-cpp)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})

find_package(
  Python3
  COMPONENTS Interpreter
  REQUIRED)

execute_process(
  COMMAND ${Python3_EXECUTABLE} -c "import pytest"
  RESULT_VARIABLE PYTEST_EXIT_CODE
  OUTPUT_QUIET)

find_package(GTest)
if(GTest_FOUND AND (NOT "${PYTEST_EXIT_CODE}"))
  enable_testing()
endif()

find_package(ClangFormat)

set(RVV_FLAGS
    -Wno-builtin-macro-redefined
    -D__DATE__="redacted"
    -D__TIMESTAMP__="redacted"
    -D__TIME__="redacted"
    -fmerge-all-constants
    -Wall
    -Wextra
    -Wconversion
    -Wsign-conversion
    -Wvla
    -Wnon-virtual-dtor)

if(NOT DEFINED RISCV_ARCH)
  set(RISCV_ARCH rv64gc_v1p0_zvfh)
endif()
list(APPEND RVV_FLAGS -march=${RISCV_ARCH})
if(${CMAKE_CXX_COMPILER_ID} MATCHES "Clang")
  list(APPEND RVV_FLAGS -menable-experimental-extensions)
endif()

set(GENERATED_INCLUDE_DIR ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_directory_properties(PROPERTY ADDITIONAL_CLEAN_FILES
                         ${GENERATED_INCLUDE_DIR})

set(GENERATOR_DIR ${PROJECT_SOURCE_DIR}/generator)
file(GLOB_RECURSE GENERATOR_LIB_SOURCES ${GENERATOR_DIR}/codegen/*.py)

macro(generate_rvv filename generator)
  set(_policy_variant ${ARGN})
  set(_cmd_arg)
  list(APPEND _cmd_arg "${GENERATED_INCLUDE_DIR}")
  set(_all_generated)
  macro(add_generated_file variant file_path)
    if("${variant}" STREQUAL "")
      list(APPEND _cmd_arg --base)
    else()
      list(APPEND _cmd_arg --${variant})
    endif()
    list(APPEND _cmd_arg ${file_path})
    set(_full_path ${GENERATED_INCLUDE_DIR}/${file_path})
    list(APPEND _all_generated ${_full_path})
    get_filename_component(EXTENSION ${_full_path} LAST_EXT)
    if(EXTENSION STREQUAL ".h")
      list(APPEND GENERATED_HEADER_FILES ${_full_path})
    else()
      list(APPEND GENERATED_INC_FILES ${_full_path})
    endif()
  endmacro()

  set(_generator_file_name ${GENERATOR_DIR}/${generator})
  add_generated_file("" rvv/${filename})

  foreach(v ${_policy_variant})
    add_generated_file(${v} rvv/policy/${v}/${filename})
  endforeach()

  add_custom_command(
    OUTPUT ${_all_generated}
    COMMAND Python3::Interpreter ${_generator_file_name} ${_cmd_arg}
    COMMAND $<IF:$<BOOL:${CLANG_FORMAT_FOUND}>,${CLANG_FORMAT_EXECUTABLE},true>
            -i ${_all_generated}
    DEPENDS ${_generator_file_name} ${GENERATOR_LIB_SOURCES}
    VERBATIM)
endmacro()

generate_rvv("type.inc" "gen_type_inc.py")
generate_rvv("misc.h" "gen_misc_h.py")
generate_rvv("load_store.h" "gen_load_store_h.py" "tu" "mu" "tumu")
generate_rvv("int.h" "gen_int_h.py" "tu" "mu" "tumu")
generate_rvv("fixed.h" "gen_fixed_h.py" "tu" "mu" "tumu")

add_custom_target(generated_files ALL DEPENDS ${GENERATED_HEADER_FILES}
                                              ${GENERATED_INC_FILES})
message("Generated files: ${GENERATED_HEADER_FILES}")
install(DIRECTORY ${GENERATED_INCLUDE_DIR}/rvv include/rvv TYPE INCLUDE)

macro(rvv_add_executable exe)
  add_executable(${exe} ${ARGN})
  add_dependencies(${exe} generated_files)
  target_compile_options(${exe} PRIVATE ${RVV_FLAGS})
  target_include_directories(${exe} PRIVATE ${GENERATED_INCLUDE_DIR} include)
  if(NOT DEFINED _FIRST_EXECUTABLE_TARGET)
    set(_FIRST_EXECUTABLE_TARGET ${exe})
    target_precompile_headers(${exe} PRIVATE ${GENERATED_HEADER_FILES})
  else()
    target_precompile_headers(${exe} REUSE_FROM ${_FIRST_EXECUTABLE_TARGET})
  endif()
endmacro()

macro(rvv_add_test exe)
  rvv_add_executable(${exe} ${ARGN})
  target_include_directories(${exe} PRIVATE GTest::GTest GTest::Main)
  target_link_libraries(${exe} GTest::GTest GTest::Main)
  add_test(NAME ${exe} COMMAND $<TARGET_FILE:${exe}>)
endmacro()

add_test(
  NAME python_tests
  COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}
  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/generator)

file(GLOB_RECURSE CPP_TESTS test/*.cpp)

foreach(test_file ${CPP_TESTS})
  get_filename_component(test_name ${test_file} NAME_WE)
  rvv_add_test(${test_name} ${test_file})
endforeach()

file(GLOB_RECURSE CPP_COMPILE_TEST compile_test/*.cpp)

rvv_add_test(compile_test ${CPP_COMPILE_TEST})
target_include_directories(compile_test
                           PRIVATE ${PROJECT_SOURCE_DIR}/compile_test)
