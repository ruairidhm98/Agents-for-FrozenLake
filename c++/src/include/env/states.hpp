#pragma once

#include "globals.hpp"

class State
{
protected:
  double m_reward;
  std::vector<int> allowableActions;
public:
  virtual void process() = 0;
  virtual char getLabel() const = 0;
};

class Hole : public State
{
public:
  Hole(double reward)
  {
    State::m_reward = m_reward;
  }
  virtual void process() override
  {

  }

  virtual char getLabel() const override
  {
    return 'H';
  }
};

class Exit : public State
{
public:
  Exit()
  {

  }
  virtual void process() override
  {

  }

  virtual char getLabel() const override
  {
    return 'E';
  }
};

class Frozen : public State
{
public:
  Frozen()
  {

  }
  virtual void process() override
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
  virtual void process() override
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
  virtual void process() override
  {

  }
  virtual char getLabel() const override
  {

  }
}