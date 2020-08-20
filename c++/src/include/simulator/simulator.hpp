#pragma once

class Agent;
class FrozenLake;

template <unsigned verbose>
class SimRunner
{
private:
  Agent &m_agent;
  FrozenLake &m_env;
public:
  void runTrial();

};
