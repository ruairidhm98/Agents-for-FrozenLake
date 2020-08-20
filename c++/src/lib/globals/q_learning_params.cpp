#include "globals/q_learning_params.hpp"

QLearningParams::QLearningParams(double gamma, unsigned ne, double rplus, double alpha)
  : m_gamma(gamma)
  , m_ne(ne)
  , m_rPlus(rplus)
  , m_alpha(alpha)
{}

double QLearningParams::getGamma() const
{
  return m_gamma;
}

unsigned QLearningParams::getNe() const
{
  return m_ne;
}

double QLearningParams::getRplus() const
{
  return m_rPlus;
}

double QLearningParams::getAlpha() const
{
  return m_alpha;
}
