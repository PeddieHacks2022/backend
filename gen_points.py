
import cv2
import posenet
import tensorflow.compat.v1 as tf

INPUT_FILE = './data/test.mp4'
SCALE_FACTOR = 0.4
MIN_POSE_SCORE=0.25

def main():

    capture = cv2.VideoCapture(INPUT_FILE)
    if not capture.isOpened():
        print("unable to read video")
        
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height  = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"video dimensions {width} x {height}")

    with tf.Session() as session:
        cfg, output = posenet.load_model(101, session)
        output_stide = cfg['output_stride']
        print(output_stide)

        res, image = capture.read()

        # put training through model
        input_image, draw_image, output_scale = posenet.read_cap(capture, scale_factor=SCALE_FACTOR, output_stride=output_stide)
        heatmaps, offsets, fwd, bwd = session.run(output, feed_dict={'image:0': input_image})

        pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
            heatmaps.squeeze(axis=0),
            offsets.squeeze(axis=0),
            fwd.squeeze(axis=0),
            bwd.squeeze(axis=0),
            output_stride=output_stide,
            min_pose_score=MIN_POSE_SCORE
        )
        print(keypoint_coords)

if __name__ == "__main__":
    main()
