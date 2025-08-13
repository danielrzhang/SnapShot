# SnapShot
SnapShot is a Python application designed to analyze video clips from hockey games. It relies on YOLO object detection, custom machine learning models, and recognition models trained from Roboflow datasets, and this tool automatically annotates key elements found in the video. This program processes input videos frame-by-frame, applies computer vision techniques for detection and tracking via a deep convolutional neural network, and outputs annotated videos with statistical summaries. This app is best used for clips from 30 seconds to 120 seconds to ensure quick processing times and accurate results. SnapShot can be used for coaches, analysts, or hockey enthusiasts to efficiently break down gameplay dynamics.

Watch a sample of SnapShot in action:
### Before SnapShot processing
[](https://github.com/user-attachments/assets/7fd4311b-6692-468c-8a49-b977d13f9174)

### After SnapShot processing
[](https://github.com/user-attachments/assets/9523a3b1-15fc-441a-8618-b74015f6869b)

## Features
* **Player Annotation by Team**: Detects and labels players from two opposing teams with position markers and team-specific identifiers via zero-shot classification
* **Puck Position Tracking**: Identifies the puck's location in each frame and estimated trajectories for visualization
* **Puck Possession Detection**: Determines which player or team has control of the puck based on proximity and movement analysis
* **Rink Keypoint Detection**: Identifies keypoints on the hockey rink (e.g. center ice, blue lines, goa lines) for perspective correction, zone identification, and enhanced spatial analytics
* **Pass and Interception Detection**: Counts sucessful passes within each team and interceptions when possession switches from opponent action
* **Puck Possession Percentage**: Calculates the percentage of time each team possess the puck for over the clip's duration
* **Customizable Training Models**: Uses Roboflow datasets and a custom YOLO-trained model for object detection

## YOLO Training Summary
The training was conducted locally on my computer for all three image classification models (puck, player, rink). Below is the specified hardware I used to achieve the reported training times. The publicly available Roboflow datasets and fine-tuning models used are also listed below.

⚠️ Be advised that if you plan on running these training models locally, a GPU is necessary. Processing solely via CPU will significantly increase training time and you may encounter device overheating issues.

**Training Device Specs:**
  * **CPU**: Intel(R) Core(TM) Ultra 7
  * **GPU**: NVIDIA RTX 3000 Ada

**Player Recognition Training Time:**
  * 18 hours

**Puck Recognition Training Time:**
  * 56 hours

**Rink Keypoints Training Time:**
  * 12 hours

**Datasets used:**
  * **Player (YOLOv5)**: https://universe.roboflow.com/francisco-workspace/hockey-3fz5i/dataset/7
  * **Puck (YOLOv5)**: https://universe.roboflow.com/rapid-q94xs/puck-detection-4/dataset/5
  * **Rink (YOLOv8)**: https://universe.roboflow.com/hockeycv-hpnix/hockeycv

**Fine-tuning data models used:**
* **Player and Puck**: https://huggingface.co/spaces/SimulaMet-HOST/HockeyAI/tree/main
* **Rink**: https://huggingface.co/SimulaMet-HOST/HockeyRink/tree/main

## Requirements
* Python 3.13
* Dependencies:
  * Ultralytics YOLO
  * PyTorch
  * Roboflow
  * OpenCV
  * NumPy

## Work In Progress
* **Improved Puck Detection**: Improve the puck detection tracking accuracy when the puck is moving at a high rate of speed, which is currently limited by camera frame rate. Advanced prediction algorithms for puck localization will need to be implemented.
* **Tactical Overview**: Implement a homography-based transformation using rink keypoints to generate a real-time overhead view of the rink to visualize player positions, puck trajectories, and team offense/defense patterns for tactical analysis
* **Offside Detection**: Add rule-based logic on top of player and puck tracking to detect offside violations, flagging when players enter the offensive zone aheda of the puck relative to blue line keypoints
* **Icing Detection**: Integrate detection for icing calls by monitoring puck shots from behind the centre line crossing the opponent's goal line without touches
* **Goal Detection and Shot Analytics**: Incorporate detection of goals by monitoring puck proximity to goal lines and nets, along with shot speed calculations

## License
This project is licensed under the GNU Public General License. See LICENSE for details.
