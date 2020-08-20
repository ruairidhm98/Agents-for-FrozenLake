#pragma once

#include "globals/globals.hpp"

#include <boost/math/distributions/uniform.hpp>

#include <array>
#include <utility>

class StateMisc
{
protected:
  char m_label;
  bool m_curState;
  double m_reward;
public:
  StateMisc(char label, bool curState, double reward)
    : m_label(label)
    , m_curState(curState)
    , m_reward(reward)
  {}

  char getLabel() const
  {
    return m_curState ? 'X' : m_label;
  }

  bool getIsCurrentState() const
  {
    return m_curState;
  }

  double getReward() const
  {
    return m_reward;
  }

  void setLabel(char label)
  {
    m_label = label;
  }

  void setIsCurrentState(bool curState)
  {
    m_curState = curState;
  }

  const StateMisc &operator=(const StateMisc &other)
  {
    if (this != &other)
    {
      m_reward = other.m_reward;
      m_curState = other.m_curState;
      m_label = other.m_label;
    }
    return *this;
  }
};

class StateParams
{
  using TransitionModel = std::array<double, Constants::NUM_ACTIONS>;
  using Position = std::pair<unsigned,unsigned>;

protected:
  StateMisc m_params;
  TransitionModel m_transitionModel;
  std::pair<unsigned, unsigned> m_pos;
  boost::math::uniform_distribution<> m_uniform;

public:
  StateParams(StateMisc params, TransitionModel transitionModel, Position pos)
    : m_params(params)
    , m_transitionModel(transitionModel)
    , m_pos(pos)
  {}

  StateParams()
    : m_params('X', false, 0.0)
    , m_transitionModel({0.0, 0.0, 0.0, 0.0})
    , m_pos({0, 0})
  {}

  char getLabel() const
  {
    return m_params.getLabel();
  }

  double getReward() const
  {
    return m_params.getReward();
  }

  bool isCurrentState() const
  {
    return m_params.getIsCurrentState();
  }

  void setCurrentState()
  {
    m_params.setIsCurrentState(true);
  }

  void unsetCurrentState()
  {
    m_params.setIsCurrentState(false);
  }

  TransitionModel getTransitionModel() const
  {
    return m_transitionModel;
  }

  const Position &getPosition() const
  {
    return m_pos;
  }

  const StateParams &operator=(const StateParams &other)
  {
    if (this != &other)
    {
      m_params = other.m_params;
      m_transitionModel = other.m_transitionModel;
      m_pos = other.m_pos;
    }
    return *this;
  }
};

class State
{
public:
  virtual eAction process(eAction action) = 0;
  virtual char getLabel() const = 0;
  virtual const StateParams &getParams() const = 0;
  virtual ~State() = default;
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
    return m_params.getLabel();
  }

  const StateParams &getParams() const override
  {
    return m_params;
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
    return m_params.getLabel();
  }
  
  const StateParams &getParams() const override
  {
    return m_params;
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
    return m_params.getLabel();
  }
  
  const StateParams &getParams() const override
  {
    return m_params;
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
    return m_params.getLabel();
  }

  const StateParams &getParams() const override
  {
    return m_params;
  }
};
