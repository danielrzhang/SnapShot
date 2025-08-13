import numpy as np
import cv2

def create_gradient_circle(radius, color, alpha=0.7):
	size = radius * 2 + 1
	y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]
	dist = np.sqrt(x **2 + y**2)
	alpha_map = alpha * (1 - (dist / radius)**2)
	alpha_map[dist > radius] = 0
	alpha_map = np.clip(alpha_map, 0, 1) * 255
	alpha_map = alpha_map.astype(np.uint8)

	circle_img = np.zeros((size, size, 4), dtype=np.uint8)
	circle_img[:, :, :3] = color
	circle_img[:, :, 3] = alpha_map

	return circle_img

def draw_advanced_keypoint(frame, center, keypoint_id, radius, color):
	x, y = center

	gradient_radius = radius + 4
	gradient = create_gradient_circle(gradient_radius, color)
	gradient_size = gradient.shape[0]

	tx = x - gradient_radius
	ty = y - gradient_radius
	gx1 = max(0, tx)
	gy1 = max(0, ty)
	gx2 = min(frame.shape[1], tx + gradient_size)
	gy2 = min(frame.shape[0], ty + gradient_size)

	if gx1 < gx2 and gy1 < gy2:
		grad_x1 = gx1 - tx
		grad_y1 = gy1 - ty
		grad_x2 = grad_x1 + (gx2 - gx1)
		grad_y2 = grad_y1 + (gy2 - gy1)
		gradient_roi = gradient[grad_y1:grad_y2, grad_x1:grad_x2]
		roi = frame[gy1:gy2, gx1:gx2]
		alpha = gradient_roi[:, :, 3:4] / 255.0
		roi[:] = roi * (1 - alpha) + gradient_roi[:, :, :3] * alpha

	cv2.circle(frame, center, radius, color, 2)
	cv2.circle(frame, center, radius - 2, color, -1)
	cv2.circle(frame, center, radius - 1, (255, 255, 255), 1)

	label_text = f"{keypoint_id}"
	font = cv2.FONT_HERSHEY_SIMPLEX
	font_scale = 0.5
	thickness = 1

	(text_w, text_h), _ = cv2.getTextSize(label_text, font, font_scale, thickness)

	margin = 2
	bg_pts = np.array([
		[x - text_w // 2 - margin, y - radius - text_h - margin * 2],
		[x + text_w // 2 + margin, y - radius - text_h - margin * 2],
		[x + text_w // 2 + margin, y - radius - margin],
		[x + margin, y - radius + margin],
		[x - margin, y - radius + margin],
		[x - text_w // 2 - margin, y - radius - margin],
	], np.int32)

	cv2.fillPoly(frame, [bg_pts], color)
	cv2.polylines(frame, [bg_pts], True, color, 1)

	cv2.putText(frame, label_text,
		(x - text_w // 2, y - radius - margin * 2),
		font, font_scale, (255, 255, 255), thickness)

class RinkKeypointsDrawer:
	def __init__(self):
		self.conf_threshold = 0.5

	def draw(self, frames, rink_keypoints):
		output_frames = []
		for index, frame in enumerate(frames):
			annotated_frame = frame.copy()
			keypoints = rink_keypoints[index]

			keypoints_numpy = keypoints.data.cpu().numpy()

			if keypoints_numpy.shape[0] == 0:
				output_frames.append(annotated_frame)
				continue

			valid_keypoints = []
			for idx, kp in enumerate(keypoints_numpy[0]):
				x, y, conf = int(kp[0]), int(kp[1]), kp[2]
				if (0 <= x < frame.shape[1] and 0 <= y < frame.shape[0] and conf > self.conf_threshold):
					valid_keypoints.append((x, y, conf, idx))

			for x, y, conf, idx in valid_keypoints:
				draw_advanced_keypoint(annotated_frame, (x, y), idx, radius=8, color = (44, 44, 255))

			output_frames.append(annotated_frame)

		return output_frames