#include "agents/agent.hpp"
#include "simulator/simulator.hpp"

#include <iostream>

using std::cout;
using std::endl;

template <unsigned verbose>
SimRunner<verbose>::SimRunner(Agent *agent, FrozenLake &env, SimRunnerConfig config)
  : m_agent(agent)
  , m_env(env)
  , m_config(config)
{}

template <unsigned verbose>
void SimRunner<verbose>::run()
{
  if constexpr(verbose)
  {
    m_agent->printDetails();
  }

  for (auto i = 0UL; i < m_config.m_numEpisodes; i++)
  {
    if constexpr(verbose)
    {
      cout << "Episode: " << i << endl;
      cout << "==========" << endl;
    }
    for (auto j = 0UL; j < m_config.m_itersPerEpisode; j++)
    {
      
    }
  }
}
