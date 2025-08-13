from .utils import draw_ellipse, draw_triangle
import webcolors

class PlayerTracksDrawer:
    def __init__(self, team_1_color, team_2_color):
        self.default_player_team_id = 1

        try:
            self.team_1_rgb = team_1_color
            self.team_2_rgb = team_2_color
            self.team_1_color = (self.team_1_rgb[2], self.team_1_rgb[1], self.team_1_rgb[0])
            self.team_2_color = (self.team_2_rgb[2], self.team_2_rgb[1], self.team_2_rgb[0])
        except ValueError as e:
            raise ValueError(f"Invalid color name: {e}. Please use valid CSS color names (e.g., red, blue, green).")

    def draw(self, video_frames, tracks, player_assignment, puck_acquisition):
        output_video_frames = []

        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            player_dict = tracks[frame_num]
            player_assignment_for_frame = player_assignment[frame_num]
            player_id_has_puck = puck_acquisition[frame_num]

            for track_id, player in player_dict.items():
                team_id = player_assignment_for_frame.get(track_id, self.default_player_team_id)

                if team_id == 1:
                    color = self.team_1_color
                else:
                    color = self.team_2_color

                if track_id == player_id_has_puck:
                    frame = draw_triangle(frame, player["bbox"], (0, 0, 255))
                    
                frame = draw_ellipse(frame, player["bbox"], color, track_id)
            output_video_frames.append(frame)

        return output_video_frames