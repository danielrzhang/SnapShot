import numpy as np
import cv2
from .homography import Homography
import sys
sys.path.append("../")
from utils import get_foot_position
 
class TacticalViewConverter:
  def __init__(self, rink_image_path):
    self.rink_image_path = rink_image_path
    self.width = 450
    self.height = 192
    self.actual_width_in_feet = 200
    self.actual_height_in_feet = 85
    
    self.key_points = [
      (0, 28.5),
      (0, 56.5),
      (11, 0),
      (11, 31.5),
      (11, 38.5),
      (11, 46.5),
      (11, 53.5),
      (11, 85),
      (15.5, 38.5),
      (15.5, 46.5),
      (29.5, 5.5),
      (29.5, 35.5),
      (29.5, 49.5),
      (29.5, 79.5),
      (31, 20.5),
      (31, 64.5),
      (32.5, 5.5),
      (32.5, 35.5),
      (32.5, 49.5),
      (32.5, 79.5),
      (75, 0),
      (75, 85),
      (80, 20.5),
      (80, 64.5),
      (100, 0),
      (100, 27.5),
      (100, 42.5),
      (100, 57.5),
      (90, 85),
      (100, 75),
      (100, 85),
      (110, 85),
      (120, 20.5),
      (120, 64.5),
      (125, 0),
      (125, 85),
      (167.5, 5.5),
      (167.5, 35.5),
      (167.5, 49.5),
      (167.5, 79.5),
      (169, 20.5),
      (169, 64.5),
      (170.5, 5.5),
      (170.5, 35.5),
      (170.5, 49.5),
      (170.5, 79.5),
      (184.5, 38.5),
      (184.5, 46.5),
      (189, 0),
      (189, 31.5),
      (189, 38.5),
      (189, 46.5),
      (189, 53.5),
      (189, 85),
      (200, 28.5),
      (200, 56.5)
    ]
    
    scale_x = self.width / self.actual_width_in_feet
    scale_y = self.height / self.actual_height_in_feet
    for i in range(len(self.key_points)):
      x, y = self.key_points[i]
      self.key_points[i] = (x * scale_x, y * scale_y)
      
  def transform_players_to_tactical_view(self, keypoints_list, player_tracks):
    tactical_player_positions = []
    
    for frame_idx, (frame_keypoints, frame_tracks) in enumerate(zip(keypoints_list, player_tracks)):
      tactical_positions = {}

      try:
        keypoints_list = frame_keypoints.xy.tolist()
        if not keypoints_list:
          tactical_player_positions.append(tactical_positions)
          continue
        frame_keypoints = keypoints_list[0]
      except (AttributeError, IndexError) as e:
        tactical_player_positions.append(tactical_positions)
        continue
      
      if frame_keypoints is None or len(frame_keypoints) == 0:
        tactical_player_positions.append(tactical_positions)
        continue
      
      detected_keypoints = frame_keypoints
      valid_indices = [i for i, keypoint in enumerate(detected_keypoints) if keypoint[0] > 0 and keypoint[1] > 0]
      
      if len(valid_indices) < 4:
        tactical_player_positions.append(tactical_positions)
        continue
      
      source_points = np.array([detected_keypoints[i] for i in valid_indices], dtype = np.float32)
      target_points = np.array([self.key_points[i] for i in valid_indices], dtype = np.float32)
      
      try:
        homography = Homography(source_points, target_points)
        
        for player_id, player_data in frame_tracks.items():
          bbox = player_data["bbox"]
          player_position = np.array([get_foot_position(bbox)])
          tactical_position = homography.transform_points(player_position)
          tactical_positions[player_id] = tactical_position[0].tolist()
        
      except (ValueError, cv2.error) as e:
        pass
        
      tactical_player_positions.append(tactical_positions)
      
    return tactical_player_positions
