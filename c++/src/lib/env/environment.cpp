#include "env/environment.hpp"
#include "globals/globals.hpp"

#include <boost/algorithm/string.hpp>

#include <fstream>
#include <iostream>
#include <string>

using std::cout;
using std::endl;
using std::getline;
using std::ifstream;
using std::make_unique;
using std::string;
using std::vector;

FrozenLake::FrozenLake(string file)
{
  ifstream fStream(file);
  processEnvMetaData(fStream);
  processEnvMap(fStream);
}

// The first line of the input file MUST be in format
// nRow nCol 
void FrozenLake::processEnvMetaData(ifstream &stream)
{
  string line;
  vector<string> splitLine;
  getline(stream, line);
  Helpers::splitWord(line, splitLine);
  m_dimensions.first = atoi(splitLine[0].c_str());
  m_dimensions.second = atoi(splitLine[1].c_str());
}

void FrozenLake::processEnvMap(ifstream &stream)
{
  string line;
  vector<string> splitLine;
  int nCol = 0, nRow = 0;
  while (getline(stream, line))
  {
    Helpers::splitWord(line, splitLine);
    for (const auto &word : splitLine)
    {
      if (word == "H" || word == "G")
      {
        m_env[nRow][nCol] = make_unique<Exit>();
        if (word == "H")
        {
          m_terminalStates.push_back((m_env[nRow][nCol]).get());
        }
        else
        {
          m_goalState = (m_env[nRow][nCol]).get();
        }
      }
      else if (word == "F" || word == "S")
      {
        m_env[nRow][nCol] = make_unique<Frozen>();
        if (word == "S")
        {
          m_startingState = (m_env[nRow][nCol]).get();
        }
      }
      ++nCol;
    }
    ++nRow;
  }
}

const State *FrozenLake::getState(unsigned i, unsigned j) const
{
  return (m_env[i][j]).get();
}

const State *FrozenLake::getCurrentState() const
{
  return m_currentState;
}

const State *FrozenLake::getGoalState() const
{
  return m_goalState;
}

const State *FrozenLake::getStartingState() const
{
  return m_startingState;
}

const State *FrozenLake::next(eAction action)
{
  auto pos = m_currentState->getParams().getPosition();
  actionToIndexMove(action, pos);
  return (m_env[pos.first][pos.second]).get();
}

void FrozenLake::print() const
{
  for (const auto &states : m_env)
  {
    for (const auto &state : states)
    {
      cout << state->getLabel();
    }
    cout << endl;
  }
}
