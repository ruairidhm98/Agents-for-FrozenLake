// Contains the agent interface to
#pragma once

#include "globals/globals.hpp"

class Agent
{
public:
  virtual eAction learn() = 0;
};
