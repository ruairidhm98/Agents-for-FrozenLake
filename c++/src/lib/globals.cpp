#include "globals/globals.hpp"

#include <boost/algorithm/string.hpp>

using boost::is_any_of;
using boost::algorithm::trim;
using boost::algorithm::split;

using std::string;
using std::vector;

static const constexpr unsigned Constants::NUM_ACTIONS = 4;

namespace Helpers
{
  void splitWord(string &line, vector<string> &splitLine)
  {
    trim(line);
    split(splitLine, line, boost::is_any_of(", "));
  }
}