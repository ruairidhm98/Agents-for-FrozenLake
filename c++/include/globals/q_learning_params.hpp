#pragma once

class QLearningParams
{
private:
  double m_gamma;
  unsigned m_ne;
  double m_rPlus;
  double m_alpha;
public:
  QLearningParams(double gamma, unsigned ne, double rplus, double alpha);
  QLearningParams(const QLearningParams &other);
  // Getters and setters
  double getGamma() const;
  unsigned getNe() const;
  double getRplus() const;
  double getAlpha() const;
  void print() const;
  const QLearningParams &operator=(const QLearningParams &other);
  ~QLearningParams();
};

