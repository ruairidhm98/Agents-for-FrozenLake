#include "agents/q_agent.hpp"

#include <iostream>

using std::cout;
using std::endl;
using std::make_pair;

QLearningAgent::QLearningAgent(QLearningParams params, FrozenLake &env)
  : m_env(env)
  , m_params(params)
  , m_currentState(nullptr)
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
  auto &&pos = m_currentState->getParams();
  return {};
}

eAction QLearningAgent::learn()
{
  return eAction::NO_ACTION;
}

void QLearningAgent::setCurrentState(State *s)
{
  m_currentState = s;
}

void QLearningAgent::printDetails() const
{
  cout << "Agent: Q-Learner" << endl;
  m_params.print();
}