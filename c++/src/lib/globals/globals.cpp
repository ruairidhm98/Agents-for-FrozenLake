#include "globals/globals.hpp"

#include <boost/algorithm/string.hpp>
#include <boost/math/distributions/uniform.hpp>
#include <boost/random.hpp>

#include <algorithm>
#include <chrono>

using boost::is_any_of;
using boost::algorithm::trim;
using boost::algorithm::split;

using std::chrono;
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

  eAction generateNextAction(eAction action, vector<eAction> &allowableActions)
  {
    // We move with 0.5 probability in the right direction 0.5 otherwise
    std::time_t now = steady_clock::now();
    boost::random::mt19937 gen{static_cast<std::uint32_t>(now)};
    boost::random::uniform_int_distribution<> dist{1, 100};

    auto acceptance = uniform(gen);
    if (acceptance <= 0.5)
    {
      return action;
    }
    else
    {
      return sample(allowableActions.begin(), allowableActions.end(), 1);
    }
  }
}
