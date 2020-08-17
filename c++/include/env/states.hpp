#pragma once

class StateParams
{

};

class State
{
public:
  virtual void process();
};

class Hole : public State
{
public:
  virtual void process() override
  {

  }
};

class Exit : public State
{
public:
  virtual void process() override
  {

  }
};

class Frozen : public State
{
public:
  virtual void process() override
  {

  }
};

class Goal : public State
{
public:
  virtual void process() override
  {

  }
};
