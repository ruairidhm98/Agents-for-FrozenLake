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

QLearningParams::QLearningParams(const QLearningParams &other)
  : m_gamma(other.m_gamma)
  , m_ne(other.m_ne)
  , m_rPlus(other.m_rPlus)
  , m_alpha(other.m_alpha)
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

const QLearningParams &QLearningParams::operator=(const QLearningParams &other)
{
  if (this != &other)
  {
    m_gamma = other.m_gamma;
    m_ne = other.m_ne;
    m_rPlus = other.m_rPlus;
    m_alpha = other.m_alpha;
  }
  return *this;
}

void QLearningParams::print() const
{
  cout << "Gamma: " << m_gamma << endl;
  cout << "Ne: " << m_ne << endl;
  cout << "RPlus: " << m_rPlus << endl;
  cout << "Alpha: " << m_alpha << endl;
}