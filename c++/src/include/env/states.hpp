#pragma once

#include "globals/globals.hpp"

#include <array>
#include <boost/math/distributions/uniform.hpp>
#include <utility>

class StateParams
{
protected:
  double m_reward;
  // Action - Transition model probability
  std::array<std::pair<eAction, double>, Constants::NUM_ACTIONS> m_allowableActions;
  boost::math::uniform_distribution<> m_uniform;
public:
  StateParams(double reward, std::array<std::pair<eAction, double> allowableActions)
  {

  }
};

class State
{
public:
  virtual eAction process(eAction action) = 0;
  virtual char getLabel() const = 0;
};

class Hole : public State
{
private:
  StateParams m_params;
public:
  Hole(StateParams params)
    : m_params(params)
  {
  }
  // If we are in a hole state, then we must exit
  virtual eAction process(eAction action) override
  {
    return eActions::NO_ACTION;
  }

  virtual char getLabel() const override
  {
    return 'H';
  }
};

class Frozen : public State
{
public:
  Frozen()
  {

  }
  virtual eAction process(eAction action) override
  {

  }

  virtual char getLabel() const override
  {
    return 'F';
  }
};

class Goal : public State
{
public:
  Goal()
  {

  }
  virtual eAction process(eAction) override
  {

  }

  virtual char getLabel() const override
  {
    return 'G';
  }
};

class Start : public State
{
public:
  virtual eAction process(eAction) override
  {

  }
  virtual char getLabel() const override
  {
    return 'S';
  }
};
