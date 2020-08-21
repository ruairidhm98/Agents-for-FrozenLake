// Contains the agent interface to
#pragma once

#include "globals/globals.hpp"

class State;

class Agent
{
public:
  virtual eAction learn() = 0;
  virtual void printDetails() const = 0;
  virtual void setCurrentState(State *state) = 0;
  virtual State *getCurrentState() const;
};
