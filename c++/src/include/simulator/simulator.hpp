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

// Compile both so we don't have to check if verbose at runtime if there is no need
class SimRunner<0>;
class SimRunner<1>;
