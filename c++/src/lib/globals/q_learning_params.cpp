#include "globals/q_learning_params.hpp"

#include <iostream>

using std::cout;
using std::endl;

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

void QLearningParams::print() const
{
  cout << "Gamma: " << m_gamma << endl;
  cout << "Ne: " << m_ne << endl;
  cout << "RPlus: " << m_rPlus << endl;
  cout << "Alpha: " << m_alpha << endl;
}