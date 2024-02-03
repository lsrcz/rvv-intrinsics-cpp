cmake_minimum_required(VERSION 3.10)
project(rvv-intrinsics-cpp)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(GTest)
if(GTest_FOUND)
  enable_testing()
endif()

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
  set(RISCV_ARCH rv64gc_v1p0)
endif()
list(APPEND RVV_FLAGS -march=${RISCV_ARCH})
if(${CMAKE_CXX_COMPILER_ID} MATCHES "Clang")
  list(APPEND RVV_FLAGS -menable-experimental-extensions)
endif()

install(DIRECTORY include/rvv TYPE INCLUDE)

macro(rvv_add_executable exe)
  add_executable(${exe} ${ARGN})
  target_compile_options(${exe} PRIVATE ${RVV_FLAGS})
  target_include_directories(${exe} PRIVATE include)
endmacro()

macro(rvv_add_test exe)
  rvv_add_executable(${exe} ${ARGN})
  target_include_directories(${exe} PRIVATE GTest::GTest GTest::Main)
  target_link_libraries(${exe} GTest::GTest GTest::Main)
  add_test(NAME ${exe} COMMAND $<TARGET_FILE:${exe}>)
endmacro()

rvv_add_test(type_test test/type_test.cpp)
rvv_add_test(type_traits_test test/type_traits_test.cpp)
