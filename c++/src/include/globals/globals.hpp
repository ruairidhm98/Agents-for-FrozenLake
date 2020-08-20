#pragma once

#include <exception>
#include <string>
#include <vector>

enum class eAction : int
{
  DOWN,
  LEFT,
  RIGHT,
  UP,
  NO_ACTION
};

namespace Constants
{
  static const constexpr unsigned NUM_ACTIONS;
}

namespace Helpers
{
  void splitWord(std::string &line, std::vector<std::string> &splitLine);
}
