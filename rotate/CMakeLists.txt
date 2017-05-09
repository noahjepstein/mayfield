project("Mayfield -- rotate")
cmake_minimum_required(VERSION 3.7)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -std=c++11 -Wall -Wextra -Werror")

add_executable(rotate
               src/rotate.cpp)