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

  vector<eAction> actionsInState();
  double exploration(double u, unsigned n) const;
public:
  QLearningAgent(QLearningParams params, FrozenLake &env);
  eAction learn() override;
  void printDetails() const override;
  void setCurrentState(State *state) override;
  State *getCurrentState() const override;
  ~QLearningAgent();
};
