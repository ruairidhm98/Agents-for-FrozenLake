#include "env/environment.hpp"
#include "globals/globals.hpp"

#include <boost/algorithm/string.hpp>

#include <fstream>
#include <iostream>
#include <string>

using std::getline;
using std::ifstream;
using std::make_unique;
using std::string;
using std::vector;

FrozenLake::FrozenLake(string file)
{
  ifstream fStream(file);
  ProcessEnvMetaData(fStream);
  ProcessEnvMap(fStream);
}

// The first line of the input file MUST be in format
// nRow nCol 
void FrozenLake::ProcessEnvMetaData(ifstream &stream)
{
  string line;
  vector<string> splitLine;
  getline(stream, line);
  splitWord(line, splitLine);
  m_dimensions.first = atoi(splitLine[0].c_str());
  m_dimensions.second = atoi(splitLine[1].c_str());
}

void FrozenLake::ProcessEnvMap(ifstream &stream)
{
  string line;
  vector<string> splitLine;
  int nCol = 0, nRow = 0;
  while (getline(stream, line))
  {
    splitWord(line, splitLine);
    for (const auto &word : splitLine)
    {
      // Goal state
      if (word == "G")
      {
        m_env[nRow][nCol] = make_unique<Goal>();
      }
      // Hole state
      else if (word == "H")
      {
        m_env[nRow][nCol] = make_unique<Hole>();
        m_terminalStates.append((m_env[nRow][nCol]).get())
      }
      // Start state or frozen (the start must be frozen...)
      else if (word == "S")
      {
        m_env[nRow][nCol] = make_unique<Frozen>();
        m_startingState = (m_env[nRow][nCol]).get();
      }
      ++nCol;
    }
    ++nRow;
  }
}

State *FrozenLake::getState(unsigned i, unsigned j) const
{
  return (m_env[i][j]).get();
}
