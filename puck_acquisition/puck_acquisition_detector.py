import sys
sys.path.append("../")
from utils import measure_distance, get_center_of_bbox

class PuckAcquisitionDetector:
  def __init__(self):
    self.possession_threshold = 100
    self.min_frames = 13
    self.containment_threshold = 0.5

  def get_key_hockey_player_assignment_points(self, player_bbox, puck_center):
    puck_center_x = puck_center[0]
    puck_center_y = puck_center[1]

    x1, y1, x2, y2 = player_bbox
    width = x2 - x1
    height = y2 - y1

    output_points = []

    if puck_center_y > y1 and puck_center_y < y2:
      output_points.append((x1, puck_center_y))
      output_points.append((x2, puck_center_y))

    if puck_center_x > x1 and puck_center_x < x2:
      output_points.append((puck_center_x, y1))
      output_points.append((puck_center_x, y2))

    output_points += [
      (x1, y1),
      (x2, y1),
      (x1, y2),
      (x2, y2),
      (x1 + width // 2, y1),
      (x1 + width // 2, y2),
      (x1, y1 + height // 2),
      (x2, y1 + height // 2)
    ]
    return output_points

  def find_minimum_distance_to_puck(self, puck_center, player_bbox):
    key_points = self.get_key_hockey_player_assignment_points(player_bbox, puck_center)
    return min(measure_distance(puck_center, key_point) for key_point in key_points)

  def calculate_puck_containment_ratio(self, player_bbox, puck_bbox):
    player_x1, player_y1, player_x2, player_y2 = player_bbox
    puck_x1, puck_y1, puck_x2, puck_y2 = puck_bbox

    puck_area = (puck_x2 - puck_x1) * (puck_y2 - puck_y1)
    intersection_x1 = max(player_x1, puck_x1)
    intersection_y1 = max(player_y1, puck_y1)
    intersection_x2 = min(player_x2, puck_x2)
    intersection_y2 = min(player_y2, puck_y2)

    if intersection_x2 < intersection_x1 or intersection_y2 < intersection_y1:
      return 0

    intersection_area = (intersection_x2 - intersection_x1) * (intersection_y2 - intersection_y1)
    containment_ratio = intersection_area / puck_area
    return containment_ratio
  
  def find_best_candidate_for_possession(self, puck_center, player_tracks_frame, puck_bbox):
    high_containment_players = []
    regular_distance_players = []

    for player_id, player_info in player_tracks_frame.items():
      player_bbox = player_info.get("bbox", [])
      if not player_bbox:
        continue

      containment = self.calculate_puck_containment_ratio(player_bbox, puck_bbox)
      min_distance = self.find_minimum_distance_to_puck(puck_center, player_bbox)

      if containment > self.containment_threshold:
        high_containment_players.append((player_id, containment))
      else:
        regular_distance_players.append((player_id, min_distance))

    if high_containment_players:
      best_candidate = max(high_containment_players, key = lambda x: x[1])
      return best_candidate[0]
    
    if regular_distance_players:
      best_candidate = min(regular_distance_players, key = lambda x: x[1])
      if best_candidate[1] < self.possession_threshold:
        return best_candidate[0]
      
    return -1
  
  def detect_puck_possession(self, player_tracks, puck_tracks):
    num_frames = len(puck_tracks)
    possession_list = [-1] * num_frames
    consecutive_possession_count = {}

    for frame_num in range(num_frames):
      puck_info = puck_tracks[frame_num].get(1, {})

      if not puck_info:
        continue

      puck_bbox = puck_info.get("bbox", [])
      if not puck_bbox:
        continue

      puck_center = get_center_of_bbox(puck_bbox)
      best_player_id = self.find_best_candidate_for_possession(puck_center, player_tracks[frame_num], puck_bbox)

      if best_player_id != -1:
        number_of_consecutive_frames = consecutive_possession_count.get(best_player_id, 0) + 1
        consecutive_possession_count = {best_player_id: number_of_consecutive_frames}

        if consecutive_possession_count[best_player_id] >= self.min_frames:
          possession_list[frame_num] = best_player_id
      else:
        consecutive_possession_count = {}

    return possession_list