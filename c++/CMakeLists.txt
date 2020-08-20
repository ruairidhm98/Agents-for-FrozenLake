cmake_minimum_required(VERSION 3.18.1)

project(AI)
set(CMAKE_CXX_STANDARD 17)

find_package(Boost)
include_directories(${Boost_INCLUDE_DIRS})

add_subdirectory(src)
