#pragma once

#include "env/states.hpp"

#include <fstream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

using std::vector;
using std::unique_ptr;
using StateIndex = std::pair<unsigned,unsigned>;
using Dimensions = std::pair<unsigned,unsigned>;

class FrozenLake
{
private:
  State *m_goalState;
  State *m_currentState;
  State *m_startingState;
  Dimensions m_dimensions;
  vector<State*> m_terminalStates;
  vector<vector<unique_ptr<State> > > m_env;

  void processEnvMetaData(std::ifstream &stream);
  void processEnvMap(std::ifstream &stream);

public:
  FrozenLake(std::string file);
  const State *getState(unsigned i, unsigned j) const;
  const State *getCurrentState() const;
  const State *getGoalState() const;
  const State *getStartingState() const;
  const State *next(eAction action);
  void print() const;
  ~FrozenLake();
};
