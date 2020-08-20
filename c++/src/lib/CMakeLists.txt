add_library(
  agent_lib
  agents/q_agent.cpp
  env/environment.cpp
  globals/globals.cpp
  globals/q_learning_params.cpp
)
