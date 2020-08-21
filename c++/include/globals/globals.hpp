#pragma once

#include <boost/math/distributions/uniform.hpp>
#include <boost/random.hpp>

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
  static const constexpr unsigned NUM_ACTIONS = 4;
}

namespace Helpers
{
  boost::random::mt19937 gen{static_cast<unsigned>(time(NULL))};
  boost::random::uniform_int_distribution<> dist{1, 100};
  
  void splitWord(std::string &line, std::vector<std::string> &splitLine);
  void actionToIndexMove(eAction action, std::pair<unsigned,unsigned> &pos);
  eAction generateNextAction(eAction action, std::vector<eAction> &allowableActions);
}
