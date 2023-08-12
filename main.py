import flet as ft
import os
import pandas as pd
import cv2
import mediapipe as mp
import time
import numpy as np
import datetime


def main(page: ft.Page):
    def stop_recording(e):
        page.session.set('play_state', False)
        page.window_bgcolor = ft.colors.BACKGROUND
        page.bgcolor = ft.colors.BACKGROUND
    def workout_page(e):
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.STOP_ROUNDED, on_click=stop_recording
        )
        page.controls.clear()
        page.update()
    def record_and_estimate_pose(e):
        view_plane = page.session.get("plane")

        def add_pt(e):
            page.session.set("pid", pid.value)
            page.dialog.open = False
        page.navigation_bar = None
        workout_page(e)
        pid = ft.TextField(label = "ID", on_submit=add_pt, expand=True)
        #plane_switch = ft.Switch(on_change = change_view)
        plane_text = ft.Text(page.session.get('plane'))
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Participant"),
            actions=[
                pid
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dlg_modal
        page.dialog.open = True
        page.session.set('play_state', True)
        page.update()
        # Initialize MediaPipe
        mp_drawing = mp.solutions.drawing_utils
        mp_holistic = mp.solutions.holistic
        mp_facemesh = mp.solutions.face_mesh

        # Initialize OpenCV
        cap = cv2.VideoCapture(0)

        # Initialize variables for calculating time elapsed
        start_time = time.time()

        def card_container(text_list, progress_list): 
            card_sample = ft.Card()
            card_column = ft.Column()
            first_row = ft.Row()
            second_row = ft.Row()
            third_row = ft.Row()
            first_row.controls = [text_list[0], progress_list[0]]
            second_row.controls = [text_list[1], progress_list[1]]
            third_row.controls = [text_list[2], progress_list[2]]
            card_cont = ft.Container(padding = 20, width = 230)
            card_column.controls = [first_row, second_row, third_row]
            card_cont.content = card_column
            card_sample.content = card_cont
            return card_sample
        

        left_shoulder_text = ft.Text('Left Shoulder:   ')
        left_shoulder_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        left_elbow_text = ft.Text('Left Elbow:   ')
        left_elbow_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        left_wrist_text = ft.Text('Left Wrist:   ')
        left_wrist_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        left_hip_text = ft.Text('Left Hip:   ')
        left_hip_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        left_knee_text = ft.Text('Left Knee:   ')
        left_knee_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        left_ankle_text = ft.Text('Left Ankle:   ')
        left_ankle_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        right_shoulder_text = ft.Text('Right Shoulder:   ')
        right_shoulder_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        right_elbow_text = ft.Text('Right Elbow:   ')
        right_elbow_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        right_wrist_text = ft.Text('Right Wrist:   ')
        right_wrist_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        right_hip_text = ft.Text('Right Hip:   ')
        right_hip_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        right_knee_text = ft.Text('Right Knee:   ')
        right_knee_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)
        right_ankle_text = ft.Text('Right Ankle:   ')
        right_ankle_progress = ft.ProgressBar(value = 0, color = ft.colors.BLUE_100, bar_height = 10, width = 50)

        top_left_card = card_container(text_list = [left_shoulder_text, left_elbow_text, left_wrist_text],
                                       progress_list = [left_shoulder_progress, left_elbow_progress, left_wrist_progress])
        bottom_left_card = card_container(text_list = [left_hip_text, left_knee_text, left_ankle_text],
                                          progress_list = [left_hip_progress, left_knee_progress, left_ankle_progress])
        top_right_card = card_container(text_list = [right_shoulder_text, right_elbow_text, right_wrist_text],
                                        progress_list = [right_shoulder_progress, right_elbow_progress, right_wrist_progress])
        bottom_right_card = card_container(text_list = [right_hip_text, right_knee_text, right_ankle_text],
                                           progress_list = [right_hip_progress, right_knee_progress, right_ankle_progress])
        spacer1 = [ft.Text('') for i in range(25)]
        spacer2 = [ft.Text('') for i in range(50)]

        top_left_row = ft.Row(controls = [top_left_card])
        bottom_left_row = ft.Row(controls = [bottom_left_card])
        top_right_row = ft.Row(controls = [top_right_card])
        bottom_right_row = ft.Row(controls = [bottom_right_card])
        left_side = ft.Column(controls=[top_left_row] + spacer1 + [bottom_left_row], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        right_side = ft.Column(controls=[top_right_row] +spacer1 + [bottom_right_row], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        row.controls = [left_side] + spacer2 + [right_side]
        page.add(row)
        page.update()

        # Create a black background
        background_color = (30, 28, 30)  # RGB color code for #1a1c1e
        right_shoulder_angles = []
        right_elbow_angles = []
        right_wrist_angles = []
        right_hip_angles = []
        right_knee_angles = []
        right_ankle_angles = []
        left_shoulder_angles = []
        left_elbow_angles = []
        left_wrist_angles = []
        left_hip_angles = []
        left_knee_angles = []
        left_ankle_angles = []


        with mp_holistic.Holistic(min_detection_confidence=0.75, min_tracking_confidence=0.75) as holistic:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                page.bgcolor = ft.colors.TRANSPARENT
                page.window_bgcolor = ft.colors.TRANSPARENT

                # Flip the image horizontally for a selfie-view display
                image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                # Perform holistic detection
                results = holistic.process(image)


                # Placeholder for movement recognition
                if results.pose_landmarks:
                    # Get the landmarks for the shoulder, elbow, and wrist
                    left_shoulder = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
                    left_elbow = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
                    left_wrist = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
                    left_hip = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
                    left_knee = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
                    left_ankle = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
                    left_finger = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX]
                    left_toe = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]

                    right_shoulder = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
                    right_elbow = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
                    right_wrist = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
                    right_hip = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
                    right_knee = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
                    right_ankle = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
                    right_finger = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX]
                    right_toe = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]
                    nose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE]
                    left_eye = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE]
                    right_eye = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE]

                    balance_metric = abs(left_ankle.x - right_ankle.x)
                    print(f"Balance metric: {balance_metric}")
                    # Calculate mid-point between ankles
                    mid_point_x = (left_ankle.x + right_ankle.x) / 2
                    mid_point_y = (left_ankle.y + right_ankle.y) / 2

                    # Calculate spine vector (from nose to hip)
                    spine_vector = [nose.x - ((left_hip.x + right_hip.x) / 2), nose.y - ((left_hip.y + right_hip.y) / 2)]

                    # Calculate vector from mid-point between ankles to hip
                    mid_to_hip_vector = [((left_hip.x + right_hip.x) / 2) - mid_point_x, ((left_hip.y + right_hip.y) / 2) - mid_point_y]

                    # Calculate alignment by taking the difference of the vectors
                    alignment_metric = abs(spine_vector[0] - mid_to_hip_vector[0]) + abs(spine_vector[1] - mid_to_hip_vector[1])

                    print(f"Alignment metric: {alignment_metric}")



                    # Calculate the angle between the shoulder, elbow, and wrist
                    if view_plane == "Frontal Plane":
                        right_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist) # the values are flip flopped for some reason
                        left_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                        right_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow) # the values are flip flopped for some reason
                        left_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)
                        right_wrist_angle = calculate_angle(left_elbow, left_wrist, left_finger) # the values are flip flopped for some reason
                        left_wrist_angle = calculate_angle(right_elbow, right_wrist, right_finger)
                        right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee) # the values are flip flopped for some reason
                        left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                        right_knee_angle = calculate_angle(left_hip, left_knee, left_ankle) # the values are flip flopped for some reason
                        left_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                        right_ankle_angle = calculate_angle(left_knee, left_ankle, left_toe) # the values are flip flopped for some reason
                        left_ankle_angle = calculate_angle(right_knee, right_ankle, right_toe)
                    if view_plane == "Side Plane":
                        right_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist) # the values are flip flopped for some reason
                        left_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                        right_shoulder_angle = calculate_angle(right_shoulder, left_shoulder, left_elbow) # the values are flip flopped for some reason
                        left_shoulder_angle = calculate_angle(left_shoulder, right_shoulder, right_elbow)
                        right_wrist_angle = calculate_angle(left_elbow, left_wrist, left_finger) # the values are flip flopped for some reason
                        left_wrist_angle = calculate_angle(right_elbow, right_wrist, right_finger)
                        right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee) # the values are flip flopped for some reason
                        left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                        right_knee_angle = calculate_angle(left_hip, left_knee, left_ankle) # the values are flip flopped for some reason
                        left_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                        right_ankle_angle = calculate_angle(left_knee, left_ankle, left_toe) # the values are flip flopped for some reason
                        left_ankle_angle = calculate_angle(right_knee, right_ankle, right_toe)
                    else:
                        right_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist) # the values are flip flopped for some reason
                        left_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                        right_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow) # the values are flip flopped for some reason
                        left_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)
                        right_wrist_angle = calculate_angle(left_elbow, left_wrist, left_finger) # the values are flip flopped for some reason
                        left_wrist_angle = calculate_angle(right_elbow, right_wrist, right_finger)
                        right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee) # the values are flip flopped for some reason
                        left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                        right_knee_angle = calculate_angle(left_hip, left_knee, left_ankle) # the values are flip flopped for some reason
                        left_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                        right_ankle_angle = calculate_angle(left_knee, left_ankle, left_toe) # the values are flip flopped for some reason
                        left_ankle_angle = calculate_angle(right_knee, right_ankle, right_toe)
                    right_elbow_text.value = "Right Elbow: " + str(int(right_elbow_angle)) if right_elbow_angle is not np.nan else 'Right Elbow:   '
                    left_elbow_text.value = "Left Elbow: " + str(int(left_elbow_angle)) if left_elbow_angle is not np.nan else 'Left Elbow:   '
                    right_shoulder_text.value = "Right Shoulder: " + str(int(right_shoulder_angle)) if right_shoulder_angle is not np.nan else 'Right Shoulder:   '
                    left_shoulder_text.value = "Left Shoulder: " + str(int(left_shoulder_angle)) if left_shoulder_angle is not np.nan else 'Left Shoulder:   '
                    right_wrist_text.value = "Right Wrist: " + str(int(right_wrist_angle)) if right_wrist_angle is not np.nan else 'Right Wrist:   '
                    left_wrist_text.value = "Left Wrist: " + str(int(left_wrist_angle)) if left_wrist_angle is not np.nan else 'Left Wrist:   '
                    right_hip_text.value = "Right Hip: " + str(int(right_hip_angle)) if right_hip_angle is not np.nan else 'Right Hip:   '
                    left_hip_text.value = "Left Hip: " + str(int(left_hip_angle)) if left_hip_angle is not np.nan else 'Left Hip:   '

                    right_knee_text.value = "Right Knee: " + str(int(right_knee_angle)) if right_knee_angle is not np.nan else 'Right Knee:   '
                    left_knee_text.value = "Left Knee: " + str(int(left_knee_angle)) if left_knee_angle is not np.nan else 'Left Knee:   '

                    right_ankle_text.value = "Right Ankle: " + str(int(right_ankle_angle)) if right_ankle_angle is not np.nan else 'Right Ankle:   '
                    left_ankle_text.value = "Left Ankle: " + str(int(left_ankle_angle)) if left_ankle_angle is not np.nan else 'Left Ankle:   '
                    
                    right_shoulder_angles.append(right_shoulder_angle)
                    right_elbow_angles.append(right_elbow_angle)
                    right_wrist_angles.append(right_wrist_angle)
                    right_hip_angles.append(right_hip_angle)
                    right_knee_angles.append(right_knee_angle)
                    right_ankle_angles.append(right_ankle_angle)

                    left_shoulder_angles.append(left_shoulder_angle)
                    left_elbow_angles.append(left_elbow_angle)
                    left_wrist_angles.append(left_wrist_angle)
                    left_hip_angles.append(left_hip_angle)
                    left_knee_angles.append(left_knee_angle)
                    left_ankle_angles.append(left_ankle_angle)

                    right_shoulder_progress.value = int(right_shoulder_angle) / 180 if right_shoulder_angle is not np.nan else 0
                    right_elbow_progress.value = int(right_elbow_angle) / 180 if right_elbow_angle is not np.nan else 0
                    right_wrist_progress.value = int(right_wrist_angle) / 180 if right_wrist_angle is not np.nan else 0
                    right_hip_progress.value = int(right_hip_angle) / 180 if right_hip_angle is not np.nan else 0
                    right_knee_progress.value = int(right_knee_angle) / 180 if right_knee_angle is not np.nan else 0
                    right_ankle_progress.value = int(right_ankle_angle) / 180 if right_ankle_angle is not np.nan else 0
                    left_shoulder_progress.value = int(left_shoulder_angle) / 180 if left_shoulder_angle is not np.nan else 0
                    left_elbow_progress.value = int(left_elbow_angle) / 180 if left_elbow_angle is not np.nan else 0
                    left_wrist_progress.value = int(left_wrist_angle) / 180 if left_wrist_angle is not np.nan else 0
                    left_hip_progress.value = int(left_hip_angle) / 180 if left_hip_angle is not np.nan else 0
                    left_knee_progress.value = int(left_knee_angle) / 180 if left_knee_angle is not np.nan else 0
                    left_ankle_progress.value = int(left_ankle_angle) / 180 if left_ankle_angle is not np.nan else 0

                # Calculate time elapsed
                time_elapsed = time.time() - start_time
                time_elapsed = time_elapsed / 60

                # Create a blank image to draw the keypoints on
                image_height, image_width, _ = image.shape
                blank_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
                blank_image[:] = background_color

                # Draw the pose, face, hands, and iris landmarks on the blank image
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        blank_image, 
                        results.pose_landmarks, 
                        mp_holistic.POSE_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)
                    )
                if results.face_landmarks:
                    mp_drawing.draw_landmarks(
                        blank_image, 
                        results.face_landmarks, 
                        mp_facemesh.FACEMESH_TESSELATION,
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1),
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1)
                    )
                if results.left_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        blank_image, 
                        results.left_hand_landmarks, 
                        mp_holistic.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)
                    )
                if results.right_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        blank_image, 
                        results.right_hand_landmarks, 
                        mp_holistic.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)
                    )



                # Resize the image to 40% of the screen size
                screen_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                screen_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                
                blank_image = cv2.resize(blank_image, (int(screen_width), int(screen_height)))
                try:
                    nose_x, nose_y = int(nose.x * int(screen_width)), int(nose.y * int(screen_height))
                    left_eye_x, left_eye_y = int(left_eye.x * int(screen_width)), int(left_eye.y * int(screen_height))
                    right_eye_x, right_eye_y = int(right_eye.x * int(screen_width)), int(right_eye.y * int(screen_height))
                    left_shoulder_x, left_shoulder_y = int(left_shoulder.x * int(screen_width)), int(left_shoulder.y * int(screen_height))
                    right_shoulder_x, right_shoulder_y = int(right_shoulder.x * int(screen_width)), int(right_shoulder.y * int(screen_height))
                    left_hip_x, left_hip_y = int(left_hip.x * int(screen_width)), int(left_hip.y * int(screen_height))
                    right_hip_x, right_hip_y = int(right_hip.x * int(screen_width)), int(right_hip.y * int(screen_height))


                    cv2.line(blank_image, (nose_x, 0), (nose_x, int(screen_height)), (0, 0, 255), 1, lineType=cv2.LINE_AA, shift=0)
                    #cv2.line(blank_image, (0, nose_y), (int(screen_width), nose_y), (0, 0, 255), 1, lineType=cv2.LINE_AA, shift=0)
                    cv2.line(blank_image, (0, left_eye_y), (int(screen_width), left_eye_y), (255, 182, 193), 1, lineType=cv2.LINE_AA, shift=0)
                    cv2.line(blank_image, (0, right_eye_y), (int(screen_width), right_eye_y), (255, 182, 193), 1, lineType=cv2.LINE_AA, shift=0)
                    cv2.line(blank_image, (0, left_shoulder_y), (int(screen_width), left_shoulder_y), (255, 255, 0), 1, lineType=cv2.LINE_AA, shift=0)
                    cv2.line(blank_image, (0, right_shoulder_y), (int(screen_width), right_shoulder_y), (255, 255, 0), 1, lineType=cv2.LINE_AA, shift=0)
                    cv2.line(blank_image, (0, left_hip_y), (int(screen_width), left_hip_y), (0, 255, 0), 1, lineType=cv2.LINE_AA, shift=0)
                    cv2.line(blank_image, (0, right_hip_y), (int(screen_width), right_hip_y), (0, 255, 0), 1, lineType=cv2.LINE_AA, shift=0)
                except:
                    continue
                page.update()
                # Display the resulting image in a frameless window
                window_name = 'Movision Analysis'
                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow(window_name, blank_image)

                # Exit if 'q' is pressed
                if cv2.waitKey(1) == ord('q') or page.session.get('play_state') == False:
                    break

        page.controls.clear()
        page.window_bgcolor = ft.colors.BACKGROUND
        page.window_bgcolor = '#1a1c1e'
        results_page(e)
        cap.release()
        cv2.destroyAllWindows()

        angles_df = pd.DataFrame(
            {
                "Right Shoulder": right_shoulder_angles,
                "Right Elbow": right_elbow_angles,
                "Right Wrist": right_wrist_angles,
                "Right Hip": right_hip_angles,
                "Right Knee": right_knee_angles,
                "Right Ankle": right_ankle_angles,
                "Left Shoulder": left_shoulder_angles,
                "Left Elbow": left_elbow_angles,
                "Left Wrist": left_wrist_angles,
                "Left Hip": left_hip_angles,
                "Left Knee": left_knee_angles,
                "Left Ankle": left_ankle_angles,
             }
        )
        final_df = pd.DataFrame(
            {
                "Joint": [joint for joint in angles_df.columns],
                "Mean": [angles_df[joint].mean() for joint in angles_df.columns],
                "Min": [angles_df[joint].min() for joint in angles_df.columns],
                "Max": [angles_df[joint].max() for joint in angles_df.columns]
            }
        )
        final_df['Range'] = final_df['Max'] - final_df['Min']
        current_day = datetime.datetime.now()
        current_day = current_day.strftime("%Y-%m-%d %H:%M:%S")
        final_df['Date'] = current_day
        file_path = f"{pid.value}.csv"
        if os.path.exists(file_path):
            past_file = pd.read_csv(file_path)
            final_df = pd.concat([past_file, final_df])
            final_df.to_csv(file_path)
        else:
            final_df.to_csv(file_path)
        page.scroll = ft.ScrollMode.ALWAYS
        page.update()
        row = ft.ResponsiveRow(run_spacing={"md": 8})
        for joint in angles_df.columns:
            try:
                rom = angles_df[joint].dropna().max() - angles_df[joint].dropna().min()
                rom_txt = str(int(rom))
                max = angles_df[joint].dropna().max()
                max_txt = str(int(max))
                min = angles_df[joint].dropna().min()
                min_txt = str(int(min))
                chart_card = create_chart_card(x = angles_df[joint].dropna().index.to_list(), 
                                            y = angles_df[joint].dropna().to_list(),
                                            type_text = joint,
                                            value_text = [rom_txt, min_txt, max_txt])
                row.controls.append(ft.Column(col = 4,controls = [chart_card]))  
            except:
                continue
            page.add(row)
        page.floating_action_button = ft.FloatingActionButton(
            text = "Home",
            icon=ft.icons.HOME, on_click=go_home
            )
        page.snack_bar = ft.SnackBar(ft.Text(f"Results saved as {pid.value}.csv"))
        page.snack_bar.open = True

        page.update()

    def go_home(e):
        print('home')
        page.controls.clear()
        page.clean()
        page.update()
        home_page(ft.Page)
        page.update()

    def create_chart_card(x, y, type_text, value_text, line_color = ft.colors.CYAN, value_color = ft.colors.BLUE_100, text_color = ft.colors.BLUE_100):
        data_list = []
        for xs, ys in zip(x,y):
            data_list.append(ft.LineChartDataPoint(xs, ys))
        data = [ft.LineChartData(
            data_points=data_list,
            color=ft.colors.with_opacity(0.5, line_color),
            stroke_width=4,
            stroke_cap_round=True,
        )]
        chart = ft.LineChart(width = 425, height = 75,
            data_series=data, min_y = 0, max_y = 200)
        types = ft.Row(controls = [ft.Text(type_text)])
        value_txt = ft.Text("Range: " + value_text[0], color = value_color, size = 24)
        values = ft.Row(controls=[
            ft.Text("Min: " + value_text[1], color = text_color, size = 10),
            ft.Text("Max: " + value_text[2], color = text_color, size = 10)])
        column = ft.Column(controls = [types, value_txt, values,  chart])
        container = ft.Container(column, padding = 20)
        card = ft.Card(content = container, width = 450, height = 200)

        return card
    def calculate_angle(a, b, c):
        vis = (a.visibility + b.visibility + c.visibility) / 3
        if vis > 0.9:
            # Calculate the angle between three points
            a = np.array([a.x, a.y])  # First point
            b = np.array([b.x, b.y])  # Mid point
            c = np.array([c.x, c.y])  # End point

            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)

            if angle > 180.0:
                angle = 360 - angle
        else:
            angle = np.nan
        return angle
    def page_change(e):
        page.floating_action_button = ft.FloatingActionButton(
            text = "Capture",
            icon=ft.icons.CAMERA_FRONT, on_click=record_and_estimate_pose
            )
        print(page.navigation_bar.selected_index)
        if len(page.controls) > 0:
            print('popped')
            page.controls.clear()
            page.update()
        if page.navigation_bar.selected_index == 0:
            settings_page(e)
            page.update()
        if page.navigation_bar.selected_index == 1:
            home_page(e)
            page.update()
        if page.navigation_bar.selected_index == 2:
            records_page(e)
            page.update()
    def results_page(e):
        page.add(ft.VerticalDivider(opacity=0.5))
    def home_page(e):
        def change_view(e):
            current_pos = page.session.get('frontal_body_plane')
            new_pos = not current_pos
            page.session.set('frontal_body_plane', new_pos)
            print(new_pos)
            if new_pos == True:
                page.session.set("plane", 'Frontal Plane')
                page.session.set('plane_image', 'standing-up-man-front.png')
                plane_text.value = 'Frontal Plane'
                plane_image.src = 'standing-up-man-front.png'
            if new_pos == False:
                page.session.set("plane", 'Side Plane')
                page.session.set('plane_image', 'man-standing-up.png')
                plane_image.src = 'man-standing-up.png'
                plane_text.value = 'Side Plane'
            page.update()
        def get_det_conf_value(e):
            page.session.set('det_conf_value', round(det_conf_slider.value,2))
            det_conf_slider.value = page.session.get('det_conf_value')
            det_conf_value.value = str(det_conf_slider.value)
            page.update()
        def get_track_conf_value(e):
            page.session.set('track_conf_value', round(track_conf_slider.value,2))
            track_conf_slider.value = page.session.get('track_conf_value')
            track_conf_value.value = str(track_conf_slider.value)
            page.update()

        card = ft.Card()
        container = ft.Container(padding = 65)
        column = ft.Column()

        def rom_cb_pressed(e):
            rom_cb.value = not rom_cb.value
            page.update()
        def align_cb_pressed(e):
            align_cb.value = not align_cb.value
            page.update()
        def bal_cb_pressed(e):
            bal_cb.value = not bal_cb.value
            page.update()

        rom_cb = ft.Checkbox(on_change=rom_cb_pressed, value = True)
        align_cb = ft.Checkbox(on_change = align_cb_pressed)
        bal_cb = ft.Checkbox(on_change = bal_cb_pressed)

        def rom_pressed(e):
            rom_cb.value = True
            align_cb.value = False
            bal_cb.value = False
            page.update()
        def align_pressed(e):
            rom_cb.value = False
            align_cb.value = True
            bal_cb.value = False
            page.update()
        def bal_pressed(e):
            rom_cb.value = False
            align_cb.value = False
            bal_cb.value = True
            page.update()
        def gait_pressed(e):
            rom_cb.value = False
            align_cb.value = False
            bal_cb.value = False
            page.update()
        column.controls = [
            ft.Text("Modules"),
            ft.ListTile(leading = ft.Icon(ft.icons.ACCESSIBILITY), 
                                 title = ft.Text('Range of Motion'), 
                                 trailing = rom_cb,
                                 on_click=rom_pressed,
                                 tooltip= "Range of motion measures the range of joint angles across multiple joints",
                                 opacity = 0.9),
            ft.ListTile(leading = ft.Icon(ft.icons.TASK_OUTLINED), 
                                 title = ft.Text('Postural Alignment'), 
                                 trailing = align_cb,
                                 on_click=align_pressed,
                                 tooltip= "Postural alignment measures metrics such as postural alignment across multiple joints and spinal regions",
                                 opacity = 0.7),
            ft.ListTile(leading = ft.Icon(ft.icons.STAR), 
                                 title = ft.Text('Balance'), 
                                 trailing = bal_cb,
                                 on_click=bal_pressed,
                                 tooltip = 'Balance measures metrics such as Center of Mass (COM) and motion stability',
                                 opacity = 0.5)

        ]
        container.content = column
        card.content = container
        page.add(card)


        settings_card = ft.Card()
        settings_container = ft.Container(padding = 65)
        settings_column = ft.Column()
        first_row = ft.Row()
        second_row = ft.Row()
        det_conf_slider = ft.Slider(label='Detection Confidence', 
                                    expand=True, 
                                    min =0, 
                                    max = 1, 
                                    round = 2,
                                    value = 0.8 if 'det_conf_value' not in page.session.get_keys() else page.session.get('det_conf_value'), 
                                    on_change=get_det_conf_value,
                                    tooltip="Threshold for markerless motion capture to detect a joint")
        det_conf_text = ft.Text("Detection Confidence")
        det_conf_value = ft.Text(str(det_conf_slider.value if 'det_conf_value' not in page.session.get_keys() else page.session.get('det_conf_value')))
        first_row.controls = [det_conf_text, det_conf_slider, det_conf_value]

        track_conf_slider = ft.Slider(label='Tracking Confidence', 
                                    expand=True, 
                                    min =0, 
                                    max = 1, 
                                    round = 2,
                                    value = 0.8 if 'track_conf_value' not in page.session.get_keys() else page.session.get('track_conf_value'), 
                                    on_change=get_track_conf_value,
                                    tooltip="Threshold for markerless motion capture to track a joint over time")
        track_conf_text = ft.Text("Tracking Confidence")
        track_conf_value = ft.Text(str(det_conf_slider.value if 'track_conf_value' not in page.session.get_keys() else page.session.get('track_conf_value')))
        second_row.controls = [track_conf_text, track_conf_slider, track_conf_value]
        if 'frontal_body_plane' not in page.session.get_keys():
            page.session.set('frontal_body_plane', True)
        if 'plane' not in page.session.get_keys():
            page.session.set("plane", 'Frontal Plane')
        if 'plane_image' not in page.session.get_keys():
            page.session.set("plane_image", 'standing-up-man-front.png')
        def plane_switched(e):
            plane_switch.value = not plane_switch.value
            change_view(e)
            page.update()
        plane_text = ft.Text()
        plane_text.value = page.session.get('plane')
        plane_image = ft.Image(src = page.session.get('plane_image'), scale = 0.7, color = 'blue')
        plane_switch = ft.Switch(on_change = change_view)

        plane_switch_tile = ft.ListTile(leading = plane_image, title = plane_text, trailing=plane_switch, on_click=plane_switched)

        settings_column.controls = [
            ft.Text("Motion Capture Settings"),
            plane_switch_tile,
            first_row,
            second_row
        ]
        settings_container.content = settings_column
        settings_card.content = settings_container
        page.add(settings_card)


        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
                ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
                ft.NavigationDestination(icon=ft.icons.TASK, label="Records"),
            ], on_change = page_change, selected_index= 1
        )
        page.floating_action_button = ft.FloatingActionButton(
            text = "Capture",
            icon=ft.icons.CAMERA_FRONT, on_click=record_and_estimate_pose
        )
        page.update()
    def records_page(e):
        def search_files_for_substring(substring):
            current_directory = os.getcwd()

            # List all files in the current working directory
            files_in_directory = os.listdir(current_directory)

            # Filter only the files (exclude directories)
            files = [file for file in files_in_directory if os.path.isfile(os.path.join(current_directory, file))]

            matching_files = [file for file in files if substring in file]

            return matching_files
        def get_records(e):
            def show_data(e):
                page.floating_action_button = ft.FloatingActionButton(text = "Back", icon = ft.icons.ARROW_BACK_IOS_NEW_SHARP, on_click=page_change)
                if ft.ListTile.selected:
                    if len(page.controls) > 0:
                        page.controls.clear()
                        page.update()
                        file = str(tile.title.value) + '.csv'
                    page.add(ft.Text(str(tile.title.value)))
                    page.add(ft.VerticalDivider(opacity = 0.5))
                    df = pd.read_csv(file)
                    df = df.round(2)
                    for dates in df['Date'].unique():
                        data = df[df['Date'] == dates]
                        groups = []
                        count = 0
                        for joint in data['Joint'].unique():
                                groups.append(ft.BarChartGroup(
                                    x=count,
                                    bar_rods=[
                                        ft.BarChartRod(
                                            from_y=data[data['Joint']==joint]['Min'].iloc[0],
                                            to_y=data[data['Joint']==joint]['Max'].iloc[0],
                                            width=40,
                                            color=ft.colors.AMBER,
                                            tooltip=f"Range: {data[data['Joint']==joint]['Range'].iloc[0]}",
                                            border_radius=0,
                                        ),
                                    ],
                                ))
                                count = count + 1
                        labs = []
                        count = 0
                        for label in data['Joint'].unique():
                            labs.append(ft.ChartAxisLabel(
                                        value = count, label=ft.Container(ft.Text(label), padding=10)
                                    ))
                            count = count + 1
                        chart = ft.BarChart(
                            bar_groups=groups,
                            border=ft.border.all(1, ft.colors.GREY_400),
                            left_axis=ft.ChartAxis(
                                labels_size=40, title=ft.Text("ROM"), title_size=40
                            ),
                            bottom_axis=ft.ChartAxis(
                                labels=labs,
                                labels_size=40,
                            ),
                            horizontal_grid_lines=ft.ChartGridLines(
                                color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
                            ),
                            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
                            max_y=200,
                            interactive=True,
                            expand=True,
                        )
                        page.add(ft.Text(str(dates)))
                        page.add(ft.VerticalDivider(opacity = 0.5))
                        page.add(ft.Column(controls = [ft.Card(ft.Container(chart, expand = True, padding = 20))], alignment=ft.MainAxisAlignment.CENTER))
                        page.update()


            files = search_files_for_substring(search_field.value)
            if len(files) > 0:
                tiles = []
                tile = ft.ListTile(leading = ft.Icon(ft.icons.PERSON), 
                                            trailing = ft.Icon(ft.icons.ARROW_FORWARD_IOS),
                                            expand = True)
                for file in files:
                    tile.title = ft.Text(file[0:-4])
                    tiles.append(tile)
                tile.on_click = show_data
                results.controls = [ft.Row(controls = [tile]) for tile in tiles]
                page.update()
            else:
                ft.Text('No Results')
        results = ft.Column()
        row = ft.Row()
        search_field = ft.TextField(label = "Search Records", on_submit=get_records, expand=True, border_color = ft.colors.BLUE_100)
        search_button = ft.IconButton(ft.icons.SEARCH, on_click=get_records)
        row.controls = [search_field, search_button]
        page.add(row)
        page.add(results)
        page.scroll = ft.ScrollMode.ALWAYS


    def settings_page(e):
        def close_dlg(e):
            page.dialog.open = False
        def about_dlg(e):
            page.dialog = ft.AlertDialog(title = ft.Text("About"), 
                                         on_dismiss= close_dlg,
                                         content = ft.Text("At Movision, we are passionate about advancing healthcare through cutting-edge technology. Our mission is to provide clinicians with a revolutionary markerless motion capture system that seamlessly integrates into their clinics, unlocking new possibilities for diagnosis, treatment, and patient care."))
            page.dialog.open = True
            page.update()

        about_tile = ft.Card(ft.ListTile(leading = ft.Icon(ft.icons.QUESTION_ANSWER), 
                                 title = ft.Text('About'), 
                                 trailing = ft.Icon(ft.icons.ARROW_FORWARD_IOS),
                                 on_click=about_dlg))
        page.add(about_tile)
        help_tile = ft.Card(ft.ListTile(leading = ft.Icon(ft.icons.HELP), 
                                title = ft.Text('Help'), 
                                trailing = ft.Icon(ft.icons.ARROW_FORWARD_IOS)))
        page.add(help_tile)
        request_tile = ft.Card(ft.ListTile(leading = ft.Icon(ft.icons.ADD_TASK), 
                                   title = ft.Text('Feature Request'), 
                                   trailing = ft.Icon(ft.icons.ARROW_FORWARD_IOS)))
        page.add(request_tile)


        
    page.theme_mode = ft.ThemeMode.DARK
    page.floating_action_button = ft.FloatingActionButton(
        text = "Capture",
        icon=ft.icons.CAMERA_FRONT, on_click=record_and_estimate_pose
    )
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.TASK, label="Records"),
        ], on_change = page_change, selected_index= 1
    )
    home_page(ft.Page)

    def min_window(e):
        page.window_minimized = True
        page.update()
    def close_window(e):
        page.window_close()
    def max_window(e):
        page.window_full_screen = True
        page.update()

    page.appbar = ft.AppBar(title = ft.Text("Movision"), 
                            center_title=True,
                            actions = [
                                ft.IconButton(icon = ft.icons.CLOSE_FULLSCREEN_OUTLINED, on_click=min_window, icon_color = 'yellow'),
                                ft.IconButton(icon = ft.icons.CLOSE, on_click=close_window, icon_color='red')
                            ])
    if 'frontal_body_plane' not in page.session.get_keys():
        page.session.set('frontal_body_plane', True)
    if 'plane' not in page.session.get_keys():
        page.session.set("plane", 'Frontal Plane')
    if 'plane_image' not in page.session.get_keys():
        page.session.set("plane_image", 'standing-up-man-front.png')
        plane_text = ft.Text()


    page.window_frameless = True
    page.window_maximized = True

    page.update()


ft.app(target=main, port=os.getenv("PORT"), route_url_strategy="path"))
