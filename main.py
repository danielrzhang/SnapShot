from utils import read_video, save_video
from trackers import PlayerTracker, PuckTracker
from drawers import (
    PlayerTracksDrawer, 
    PuckTracksDrawer, 
    TeamPuckControlDrawer, 
    PassInterceptionDrawer, 
    RinkKeypointsDrawer, 
    TacticalViewDrawer)
from team_assigner import TeamAssigner
from puck_acquisition import PuckAcquisitionDetector
from pass_and_interception_detector import PassAndInterceptionDetector
from rink_keypoint_detector import RinkKeypointDetector
from tactical_view_converter import TacticalViewConverter
import webcolors

def main():
    while True:
        team_1_color_string = input("Enter the color for Team 1 (e.g., red, blue): ").strip().lower()
        try:
            team_1_color_rgb = webcolors.name_to_rgb(team_1_color_string)
            break
        except ValueError:
            print(f"'{team_1_color_string}' is not a valid CSS color name. Please try again (e.g., red, blue, green).")

    while True:
        team_2_color_string = input("Enter the color for Team 2 (e.g., green, yellow): ").strip().lower()
        try:
            team_2_color_rgb = webcolors.name_to_rgb(team_2_color_string)
            if team_2_color_string == team_1_color_string:
                print("Team 2 color must be different from Team 1 color. Please try again.")
                continue
            break
        except ValueError:
            print(f"'{team_2_color_string}' is not a valid CSS color name. Please try again (e.g., green, yellow).")

    video_frames = read_video("input-videos/nhl.mp4")

    player_tracker = PlayerTracker("models/puck-detector.pt")
    puck_tracker = PuckTracker("models/puck-detector.pt")
    rink_keypoint_detector = RinkKeypointDetector("models/rink-detector.pt")

    player_tracks = player_tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path="stubs/player_track_stubs.pkl")
    puck_tracks = puck_tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path="stubs/puck_track_stubs.pkl")
    
    rink_keypoints = rink_keypoint_detector.get_rink_keypoints(video_frames, read_from_stub = True, stub_path = "stubs/rink_keypoint_stubs.pkl")
    
    puck_tracks = puck_tracker.remove_wrong_detections(puck_tracks)
    puck_tracks = puck_tracker.interpolate_puck_positions(puck_tracks)

    team_assigner = TeamAssigner(team_1_class_name=f"{team_1_color_string} jersey", team_2_class_name=f"{team_2_color_string} jersey")
    player_assignment = team_assigner.get_player_teams_across_frames(video_frames, player_tracks, read_from_stub=True, stub_path="stubs/player_assignment_stub.pkl")

    puck_acquisition_detector = PuckAcquisitionDetector()
    puck_acquisition = puck_acquisition_detector.detect_puck_possession(player_tracks, puck_tracks)

    pass_and_interception_detector = PassAndInterceptionDetector()
    passes = pass_and_interception_detector.detect_passes(puck_acquisition, player_assignment)
    interceptions = pass_and_interception_detector.detect_interceptions(puck_acquisition, player_assignment)
    
    tactical_view_converter = TacticalViewConverter(rink_image_path="./images/nhl-hockey-rink.png")
    tactical_player_positions = tactical_view_converter.transform_players_to_tactical_view(rink_keypoints, player_tracks)

    player_tracks_drawer = PlayerTracksDrawer(team_1_color_rgb, team_2_color_rgb)
    puck_tracks_drawer = PuckTracksDrawer()
    team_puck_control_drawer = TeamPuckControlDrawer()
    pass_interception_drawer = PassInterceptionDrawer()
    rink_keypoint_drawer = RinkKeypointsDrawer()
    tactical_view_drawer = TacticalViewDrawer(team_1_color_rgb, team_2_color_rgb)

    output_video_frames = player_tracks_drawer.draw(video_frames, player_tracks, player_assignment, puck_acquisition)
    output_video_frames = puck_tracks_drawer.draw(output_video_frames, puck_tracks)
    output_video_frames = rink_keypoint_drawer.draw(output_video_frames, rink_keypoints)
    output_video_frames = team_puck_control_drawer.draw(output_video_frames, player_assignment, puck_acquisition)
    output_video_frames = pass_interception_drawer.draw(output_video_frames, passes, interceptions)
    # output_video_frames = tactical_view_drawer.draw(output_video_frames, 
    #                                                 tactical_view_converter.rink_image_path, 
    #                                                 tactical_view_converter.width, 
    #                                                 tactical_view_converter.height, 
    #                                                 tactical_view_converter.key_points,
    #                                                 tactical_player_positions,
    #                                                 player_assignment,
    #                                                 puck_acquisition)

    save_video(output_video_frames, "output-videos/nhl.avi")

if __name__ == "__main__":
    main()