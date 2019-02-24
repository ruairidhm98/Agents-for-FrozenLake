"""
A script which defines an abstract class for each of the
agents that will be used
"""
from uofgsocsai import LochLomondEnv
from abc import ABC, abstractmethod

class Agent(ABC):
  """
  Abstract class to represent and agent
  """
  def __init__(self, problem_id, is_stochastic, reward_hole):
      self.env = LochLomondEnv(problem_id=problem_id,
                               is_stochastic=is_stochastic,
                               reward_hole=reward_hole)

  @abstractmethod
  def solve_and_display(self, max_episodes, max_iter_per_episode, reward_hole):
      """
      Each type of agent which will solve the problem, will provide an
      unique implementation giving the type of agent it is
      """
      pass