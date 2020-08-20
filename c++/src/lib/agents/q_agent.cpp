#include "agents/q_agent.hpp"

using std::make_pair;

QLearningAgent::QLearningAgent(QLearningParams params, FrozenLake &env)
  : m_params(params)
  , m_currentState(make_pair(0UL, 0UL))
  , m_env(env)
{}

double QLearningAgent::exploration(double u, unsigned n) const
{
  if (n < m_params.getNe())
  {
    return m_params.getRplus();
  }
  else
  {
    return u;
  }
}

std::vector<eAction> QLearningAgent::actionsInState()
{
  State *state = m_env.getState(m_currentState.first, m_currentState.second);
  return {};
}