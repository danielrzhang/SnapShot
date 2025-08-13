import cv2
import numpy as np
from utils import get_foot_position

class TacticalViewDrawer:
  def __init__(self, team_1_color, team_2_color):
    self.start_x = 1450
    self.start_y = 40
    self.team_1_color = team_1_color
    self.team_2_color = team_2_color
  
  def draw(self, video_frames, rink_image_path, width, height, tactical_rink_keypoints, tactical_player_positions, player_assignment = None, puck_acquisition = None):
    rink_image = cv2.imread(rink_image_path, cv2.IMREAD_UNCHANGED)
    rink_image = cv2.resize(rink_image, (width, height), interpolation=cv2.INTER_AREA)
    
    rink_bgr = rink_image[:, :, :3]
    rink_alpha = rink_image[:, :, 3].astype(float) / 255.0
    
    rink_alpha = np.stack([rink_alpha] * 3, axis=2) 
    
    output_video_frames = []
    for frame_idx, frame in enumerate(video_frames):
      frame = frame.copy()
      x1 = self.start_x
      y1 = self.start_y
      x2 = x1 + width
      y2 = y1 + height
      
      if (y2 <= frame.shape[0] and x2 <= frame.shape[1] and 
        rink_image.shape[0] == y2 - y1 and rink_image.shape[1] == x2 - x1):
        roi = frame[y1:y2, x1:x2].copy()
        blended = (rink_bgr * rink_alpha + roi * (1 - rink_alpha)).astype(np.uint8)
        frame[y1:y2, x1:x2] = blended
        
      for key_point_index, keypoint in enumerate(tactical_rink_keypoints):
        x, y = keypoint
        x += self.start_x
        y += self.start_y
        # cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
        # cv2.putText(frame, str(key_point_index), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        frame_positions = tactical_player_positions[frame_idx]
        frame_assignment = player_assignment[frame_idx]
        player_with_puck = puck_acquisition[frame_idx]
        
        for player_id, position in frame_positions.items():
          team_id = frame_assignment.get(player_id)
          color = self.team_1_color if team_id == 1 else self.team_2_color
          x, y = int(position[0] + self.start_x), int(position[1] + self.start_y)
          player_radius = 3
          cv2.circle(frame, (x, y), player_radius, color, -1)
          
          if player_id == player_with_puck:
            cv2.circle(frame, (x, y), player_radius + 3, (0, 0, 255), 2)
      
      output_video_frames.append(frame)
    
    return output_video_frames