#pragma once

#include "env/states.hpp"

#include <fstream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

using StateIndex = std::pair<unsigned,unsigned>;
using Dimensions = std::pair<unsigned,unsigned>;

class FrozenLake
{
private:
  State *m_startingState;
  Dimensions m_dimensions;
  std::vector<State*> m_terminalStates;
  std::vector<std::vector<std::unique_ptr<State> > > m_env;

  // Helper functions
  void ProcessEnvMetaData(std::ifstream &stream);
  void ProcessEnvMap(std::ifstream &stream);
public:
  FrozenLake(std::string file);
  State &getState(unsigned i, unsigned j) const;
  ~FrozenLake();
};
