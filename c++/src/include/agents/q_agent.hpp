#pragma once

#include "agents/agent.hpp"
#include "env/environment.hpp"
#include "globals/q_learning_params.hpp"

#include <unordered_map>
#include <vector>

class QLearningAgent : public Agent
{
private:
  FrozenLake &m_env;
  State *m_currentState; 
  QLearningParams m_params;
  std::vector<int> m_qTable;

public:
  QLearningAgent(QLearningParams params, FrozenLake &env);
  double exploration(double u, unsigned n) const;
  std::vector<eAction> actionsInState();
  int learn() override;
  ~QLearningAgent();
};