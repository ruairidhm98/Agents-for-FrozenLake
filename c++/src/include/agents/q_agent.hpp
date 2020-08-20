#pragma once

#include "agents/agent.hpp"
#include "env/environment.hpp"
#include "globals/q_learning_params.hpp"

#include <unordered_map>
#include <vector>

using std::vector;

class QLearningAgent : public Agent
{
private:
  FrozenLake &m_env;
  vector<int> m_qTable;
  State *m_currentState; 
  QLearningParams m_params;

public:
  QLearningAgent(QLearningParams params, FrozenLake &env);
  double exploration(double u, unsigned n) const;
  std::vector<eAction> actionsInState();
  eAction learn() override;
  ~QLearningAgent();
};
