#pragma once

class Agent;
class FrozenLake;

struct SimRunnerConfig
{
  unsigned m_numEpisodes;
  unsigned m_itersPerEpisode;
};

template <unsigned verbose>
class SimRunner
{
private:
  Agent *m_agent;
  FrozenLake &m_env;
  SimRunnerConfig m_config;

  void runTrial();

public:
  SimRunner(Agent *agent, FrozenLake &env, SimRunnerConfig config);
  void run();
};
