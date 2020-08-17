#pragma once

#include "agents/agent.hpp"
#include "env/environment.hpp"
#include <unordered_map>
#include <vector>

class QLearningParams
{
private:
  double m_gamma;
  unsigned m_ne;
  double m_rPlus;
  double m_alpha;
public:
  QLearningParams(double gamma, unsigned ne, unsigned rplus, double alpha);
  // Getters and setters
  double getGamma() const;
  unsigned getNe() const;
  unsigned getRplus() const;
  double getAlpha() const;
  void setGamma(double gamma);
  void setNe(unsigned ne);
  void setRplus(unsigned rPlus);
  void setAlpha(double alpha);
  ~QLearningParams();
};

class QLearningAgent : public Agent
{
private:
  QLearningParams m_params;
  FrozenLake m_env;
  std::unordered_map<int,double> m_qTable;

public:
  QLearningAgent(QLearningParams params);
  double exploration(double u, unsigned n);
  std::vector<int> actionsInState();
  virtual int learn() override;
  ~QLearningAgent();
};