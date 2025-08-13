# SnapShot
## Overview
SnapShot is a Python application designed to analyze video clips from hockey games. It relies on YOLO object detection and custom machine learning models trained from Roboflow datasets, and this tool automatically annotates key elements found in the video. This program processes input videos frame-by-frame, applies computer vision techniques for detection and tracking, and outputs annotated videos with statistical summaries. This app is best used for clips up to 30 seconds to ensure quick processing times and highest accuracy. This can be used for coaches, analysts, or hockey enthusiasts to efficiently break down gameplay dynamics.

## Original
Watch a sample of SnapShot in action:
### Before
<video controls width="600">
  <source src="./input-videos/nhl.mp4" type="video/mp4">
</video>

### After
<video controls width="600">
  <source src="./output-videos/nhl.mp4" type="video/mp4">
</video>

## Features
* **Player Annotation by Team**: Detects and labels players from two opposing teams with position markers and team-specific identifiers
* **Puck Position Tracking**: Identifies the puck's location in each frame and estimated trajectories for visualization
* **Puck Possession Detection**: Determines which player or team has control of the puck based on proximity and movement analysis
* **Rink Keypoint Detection**: Identifies keypoints on the hockey rink (e.g. center ice, blue lines, goa lines) for perspective correction, zone identification, and enhanced spatial analytics
* **Pass and Interception Detection**: Counts sucessful passes within each team and interceptions when possession switches from opponent action
* **Puck Possession Percentage**: Calculates the percentage of time each team possess the puck for over the clip's duration
* **Customizable Training Models**: Uses Roboflow datasets and a custom YOLO-trained model for object detection

## Requirements
* Python 3.13
* Dependencies:
  * OpenCV
  * Ultralytics YOLO
  * PyTorch
  * Roboflow
  * NumPy
  * Pandas

## To-Do
* **Tactical Overview**: Implement a homography-based transformation using rink keypoints to generate a real-time overhead view of the rink to visualize player positions, puck trajectories, and team offense/defense patterns for tactical analysis
* **Offside Detection**: Add rule-based logic on top of player and puck tracking to detect offside violations, flagging when players enter the offensive zone aheda of the puck relative to blue line keypoints
* **Icing Detection**: Integrate detection for icing calls by monitoring puck shots from behind the centre line crossing the opponent's goal line without touches
* **Goal Detection and Shot Analytics**: Incorporate detection of goals by monitoring puck proximity to goal lines and nets, along with shot speed calculations

## License
This project is licensed under the GNU Public General License. See LICENSE for details.