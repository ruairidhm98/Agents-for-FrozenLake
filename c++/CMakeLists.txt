cmake_minimum_required(VERSION 3.18.1)

find_package(Boost)
include_directories(${Boost_INCLUDE_DIRS})

add_subdirectory(src)
