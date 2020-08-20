#pragma once

#include "globals/globals.hpp"

#include <boost/math/distributions/uniform.hpp>

#include <array>
#include <utility>

class StateParams
{
protected:
  double m_reward;
  std::pair<unsigned, unsigned> m_pos;
  boost::math::uniform_distribution<> m_uniform;
  std::array<double, Constants::NUM_ACTIONS> m_transitionModel;

public:
  StateParams(double reward, std::array<double,
              Constants::NUM_ACTIONS> transitionModel,
              std::pair<unsigned, unsigned> pos)
    : m_reward(reward)
    , m_transitionModel(transitionModel)
    , m_pos(pos)
  {}

  StateParams()
    : m_reward(0.0)
    , m_transitionModel({0.0, 0.0, 0.0, 0.0})
    , m_pos({0, 0})
  {}
};

class State
{
public:
  virtual eAction process(eAction action) = 0;
  virtual char getLabel() const = 0;
  ~State() = default;
};

class Hole : public State
{
private:
  StateParams m_params;
public:
  Hole(StateParams params)
    : m_params(params)
  {}

  Hole() = default;

  // If we are in a hole state, then we must exit
  virtual eAction process(eAction action) override
  {
    return eAction::NO_ACTION;
  }

  virtual char getLabel() const override
  {
    return 'H';
  }
};

class Frozen : public State
{
private:
  StateParams m_params;
public:
  Frozen(StateParams params)
    : m_params(params)
  {}

  Frozen() = default;

  virtual eAction process(eAction action) override
  {
    return eAction::LEFT;
  }

  virtual char getLabel() const override
  {
    return 'F';
  }
};

class Goal : public State
{
private:
  StateParams m_params;
public:
  Goal(StateParams params)
    : m_params(params)
  {}

  Goal() = default;

  virtual eAction process(eAction action) override
  {
    return eAction::RIGHT;
  }

  virtual char getLabel() const override
  {
    return 'G';
  }
};

class Start : public State
{
private:
  StateParams m_params;
public:
  Start(StateParams params)
    : m_params(params)
  {}

  Start() = default;

  virtual eAction process(eAction action) override
  {
    return eAction::UP;
  }
  virtual char getLabel() const override
  {
    return 'S';
  }
};
