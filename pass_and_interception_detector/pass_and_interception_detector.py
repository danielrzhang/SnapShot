class PassAndInterceptionDetector:
  def __init__(self):
    pass

  def detect_passes(self, puck_acquisition, player_assignment):
    passes = [-1] * len(puck_acquisition)
    previous_holder = -1
    previous_frame = -1

    for frame in range(1, len(puck_acquisition)):
      if puck_acquisition[frame - 1] != -1:
        previous_holder = puck_acquisition[frame - 1]
        previous_frame = frame - 1
      current_holder = puck_acquisition[frame]

      if previous_holder != -1 and current_holder != -1 and previous_holder != current_holder:
        previous_team = player_assignment[previous_frame].get(previous_holder, -1)
        current_team = player_assignment[frame].get(current_holder, -1)

        if previous_team == current_team and previous_team != -1:
          passes[frame] = previous_team
          
    return passes
  
  def detect_interceptions(self, puck_acquisition, player_assignment):
    interceptions = [-1] * len(puck_acquisition)
    previous_holder = -1
    previous_frame = -1

    for frame in range(1, len(puck_acquisition)):
      if puck_acquisition[frame - 1] != -1:
        previous_holder = puck_acquisition[frame - 1]
        previous_frame = frame - 1
      current_holder = puck_acquisition[frame]

      if previous_holder != -1 and current_holder != -1 and previous_holder != current_holder:
        previous_team = player_assignment[previous_frame].get(previous_holder, -1)
        current_team = player_assignment[frame].get(current_holder, -1)

        if previous_team != current_team and previous_team != -1 and current_team != -1:
          interceptions[frame] = previous_team

    return interceptions