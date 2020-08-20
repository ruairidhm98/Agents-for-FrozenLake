#include "globals/globals.hpp"

#include <boost/algorithm/string.hpp>

#include <algorithm>
#include <chrono>
#include <ctime>

using boost::is_any_of;
using boost::algorithm::trim;
using boost::algorithm::split;

using std::pair;
using std::sample;
using std::string;
using std::vector;

namespace Helpers
{
  void splitWord(string &line, vector<string> &splitLine)
  {
    trim(line);
    split(splitLine, line, boost::is_any_of(", "));
  }
  
  void actionToIndexMove(eAction action, pair<unsigned,unsigned> &pos)
  {
    switch(action)
    {
    case eAction::UP:
      ++pos.first;
      break;
    case eAction::DOWN:
      --pos.first;
      break;
    case eAction::LEFT:
      --pos.second;
      break;
    case eAction::RIGHT:
      ++pos.second;
    }
  }

  eAction generateNextAction(eAction action, vector<eAction> &allowableActions)
  {
    auto acceptance = static_cast<unsigned>(dist(gen));
    if (acceptance <= 50)
    {
      return action;
    }
    srand(time(NULL));
    return allowableActions[rand() % allowableActions.size()];
  }
}
