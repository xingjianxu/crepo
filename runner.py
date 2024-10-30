class Runner():
  def __init__(self, dry=False, silent=False):
    self.__dry = dry
    self.__silent = silent
    self.runned_labels = []

  def run(self, command_label, action):
    self.runned_labels.append(command_label)
    if self.__dry:
      if not self.__silent:
        print(command_label) 
    else:
      action()