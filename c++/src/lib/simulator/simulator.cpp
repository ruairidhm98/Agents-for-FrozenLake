#include "agents/agent.hpp"
#include "env/environment.hpp"
#include "simulator/simulator.hpp"

#include <iostream>

using std::cout;
using std::endl;
using std::make_pair;

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
    m_agent->setCurrentState(m_env.getStartingState());
    for (auto j = 0UL; j < m_config.m_itersPerEpisode; j++)
    {
      // Take information from percepts
      auto *currentState = m_agent->getCurrentState();
      auto &&stateParams = currentState->getParams();
      auto reward = stateParams.getReward();

      auto nextAction = m_agent->learn();

      // We are done - have reached a hole or the goal state
      if (nextAction == eAction::NO_ACTION)
      {
        break;
      }

      auto *nextState = m_env.next(nextAction);
      if (nextState->getLabel() == 'G')
      {
        cout << "Reached goal" << endl;
        cout << "Iterations: " << (j+1) << endl;
        break;
      }
      m_agent->setCurrentState(nextState);
    }
  }
}
