#pragma once

#include <exception>
#include <string>
#include <vector>

enum class eActions : int
{
  DOWN,
  LEFT,
  RIGHT,
  UP
};

namespace Helpers
{
  void splitWord(std::string &line, std::vector<std::string> &splitLine);
}
