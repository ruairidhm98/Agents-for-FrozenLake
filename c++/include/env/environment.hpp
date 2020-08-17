#pragma once

#include <string>
#include <utility>
#include <vector>

using StateIndex = std::pair<unsigned,unsigned>;

enum class eActions : int
{
  DOWN,
  LEFT,
  RIGHT,
  UP
};

struct Dimensions
{
  unsigned m_nRows;
  unsigned m_nCols;
};

class FrozenLake
{
private:
  double m_rewardHole;
  Dimensions m_dimensions;
  std::vector<std::vector<int> > m_env;
  std::vector<StateIndex> m_terminalStates;
public:
  FrozenLake(std::string file);
  ~FrozenLake();
};
