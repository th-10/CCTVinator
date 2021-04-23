def get_centres(p1):
    import numpy as np
    return np.transpose(np.array([p1[:, 0] + p1[:, 2]/2, p1[:, 1] + p1[:, 3]/2]))


def distance(p1, p2):
    import numpy as np
    p1 = np.expand_dims(p1, 0)
    if p2.ndim == 1:
        p2 = np.expand_dims(p2, 0)

    c1 = get_centres(p1)
    c2 = get_centres(p2)
    return np.linalg.norm(c1 - c2, axis=1)


def get_nearest(p1, points):
    import numpy as np
    """returns index of the point in points that is closest to p1"""
    return np.argmin(distance(p1, points))


def cut(image, coords):
    (x, y, w, h) = coords
    return image[y:y+h, x:x+w]


def overlay(frame, image, coords):
    import cv2
    (x, y, w, h) = coords
    frame[y:y+h, x:x +
          w] = cv2.addWeighted(frame[y:y+h, x:x+w], 0.5, cut(image, coords), 0.5, 0)


def sec2HMS(seconds):
    import time as tm
    return tm.strftime('%M:%S', tm.gmtime(seconds))


def frame2HMS(n_frame, fps):
    return sec2HMS(float(n_frame)/float(fps))


def processVideo(st):
    import os
    import numpy as np
    import cv2
    import time as tm
    import argparse
    import progressbar
    import box
    import moving_obj
    # parser = argparse.ArgumentParser()
    # parser.add_argument("VID_PATH", help="Path to the video to be summarized")
    # parser.add_argument("--INTERVAL_BW_DIVISIONS",
    #                     help="Interval between divisions to split the moving objects - more of this => longer video => less overlapping")
    # args = parser.parse_args()
    # In[2]:
    print(st)
    VID_PATH = st

    cap = cv2.VideoCapture(VID_PATH)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    CONTINUITY_THRESHOLD = fps  # For cutting out boxes

    MIN_SECONDS = 3  # (seconds) Minimum duration of a moving object

    # (seconds) For distributing moving objects over a duration to reduce overlapping.
    INTERVAL_BW_DIVISIONS = 10
    GAP_BW_DIVISIONS = 0.25  # (seconds)

    # if args.INTERVAL_BW_DIVISIONS:
    #     INTERVAL_BW_DIVISIONS = args.INTERVAL_BW_DIVISIONS

    # ## Extracting boxes using BGSubtraction


    """Will give boxes for each frame and simultaneously extract background"""

    fgbg = cv2.createBackgroundSubtractorKNN()

    ret, frame = cap.read()
    all_conts = []

    avg2 = np.float32(frame)  # BG-Ext

    fcount = -1

    print("Extracting bounding boxes and background...")

    with progressbar.ProgressBar(max_value=total_frames) as bar:
        while ret:

            fcount += 1

            bar.update(fcount)

            # Background extraction
            try:
                cv2.accumulateWeighted(frame, avg2, 0.01)
                # cv2.imshow('rgb', frame)
            except:
                break
            # if ret is true than no error with cap.isOpened
            ret, frame = cap.read()

            if ret == True:
                # apply background substraction
                fgmask = fgbg.apply(frame)

                # apply contours on foreground
                (contours, hierarchy) = cv2.findContours(
                    fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                contours = np.array([np.array(cv2.boundingRect(c))
                                     for c in contours if cv2.contourArea(c) >= 8000])
                all_conts.append(contours)
                for c in contours:

                    # get bounding box from countour
                    (x, y, w, h) = c

                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 255, 0), 2)

                cv2.imshow('rgb', frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                # tm.sleep(1/45)

    cap.release()
    cv2.destroyAllWindows()
    background = cv2.convertScaleAbs(avg2)

    # ## Object tracking

    """Will associate boxes into objects"""
    # old - boxes in the previous frame
    # new - boxes in the current frame

    print("Associating boxes into objects...")

    moving_objs = []

    for curr_time, new_boxes in enumerate(all_conts):  # iterating over frames
        if len(new_boxes) != 0:  # if not empty
            # all new boxes initially are not associated with any moving_objs
            new_assocs = [None]*len(new_boxes)
            obj_coords = np.array([obj.last_coords() for obj in moving_objs if obj.age(
                curr_time) < CONTINUITY_THRESHOLD])
            unexp_idx = -1  # index of unexpired obj in moving_objs
            for obj_idx, obj in enumerate(moving_objs):
                if obj.age(curr_time) < CONTINUITY_THRESHOLD:  # checking only unexpired objects
                    unexp_idx += 1
                    nearest_new = get_nearest(
                        obj.last_coords(), new_boxes)  # nearest box to obj
                    nearest_obj = get_nearest(
                        new_boxes[nearest_new], obj_coords)  # nearest obj to box

                    if nearest_obj == unexp_idx:  # both closest to each-other
                        # associate
                        new_assocs[nearest_new] = obj_idx

        for new_idx, new_coords in enumerate(new_boxes):
            new_assoc = new_assocs[new_idx]
            new_box = box.box(new_coords, curr_time)

            if new_assoc is not None:
                # associate new box to moving_obj
                moving_objs[new_assoc].add_box(new_box)
            else:
                # add a fresh, new moving_obj to moving_objs
                new_moving_obj = moving_obj.moving_obj(new_box)
                moving_objs.append(new_moving_obj)

    # Removing objects that occur for a very small duration

    MIN_FRAMES = MIN_SECONDS*fps

    moving_objs = [obj for obj in moving_objs if (
        obj.boxes[-1].time-obj.boxes[0].time) > MIN_FRAMES]

    # ## Overlaying moving objects on background

    max_orig_len = max(obj.boxes[-1].time for obj in moving_objs)
    max_duration = max((obj.boxes[-1].time - obj.boxes[0].time)
                       for obj in moving_objs)
    # max_duration of a moving_obj. This is taken as the duration of the final summary
    start_times = [obj.boxes[0].time for obj in moving_objs]

    N_DIVISIONS = int(max_orig_len/(INTERVAL_BW_DIVISIONS))

    final_video = [background.copy() for _ in range(
        max_duration+int(N_DIVISIONS*GAP_BW_DIVISIONS)+10)]  # initializing frames of final video

    """Crop moving objects from main video and overlay them on the background"""
    cap = cv2.VideoCapture(VID_PATH)
    # fgbg = cv2.createBackgroundSubtractorMOG2()

    ret, frame = cap.read()  # original video
    # all_conts = []

    all_texts = []

    vid_time = -1

    fcount = -1

    print("Cropping moving objects from the main video and overlay them on the bakground....")

    with progressbar.ProgressBar(max_value=total_frames) as bar:

        while ret:

            fcount += 1
            bar.update(fcount)

            vid_time += 1
            ret, frame = cap.read()

            if ret == True:

                for obj_idx, mving_obj in enumerate(moving_objs):
                    if mving_obj.boxes:  # non-empty
                        first_box = mving_obj.boxes[0]

                        if(first_box.time == vid_time):
                            final_time = first_box.time - start_times[obj_idx] + int(
                                int(start_times[obj_idx]/int(INTERVAL_BW_DIVISIONS*fps))*GAP_BW_DIVISIONS*fps)

                            overlay(final_video[final_time-1],
                                    frame, first_box.coords)
                            (x, y, w, h) = first_box.coords

                            #TODO: DESIGN
        #                     all_texts.append((final_time-1, frame2HMS(first_box.time, fps), (x, y-10))) #Above
                            all_texts.append(
                                (final_time-1, frame2HMS(first_box.time, fps), (x+int(w/2), y+int(h/2))))  # Centre

                            del(mving_obj.boxes[0])
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    print("Writing overlay video...")

    filename = os.path.basename(VID_PATH).split('.')[0]
    out = cv2.VideoWriter(filename+'_overlay.avi', cv2.VideoWriter_fourcc(*
                                                                          'DIVX'), fps, (background.shape[1], background.shape[0]))

    for frame in final_video:
        #cv2.imshow('Video summary',frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    #     tm.sleep(1/30) #TODO: FPS
    out.release()
    cap.release()
    cv2.destroyAllWindows()

    # annotating moving objects
    for (t, text, org) in all_texts:
        cv2.putText(final_video[t], text, org,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (252, 240, 3), 2)


    # ## Final video

    print("Writing recap Summary video...")

    filename = os.path.basename(VID_PATH).split('.')[0]
    out = cv2.VideoWriter(filename+'_summary.avi', cv2.VideoWriter_fourcc(*
                                                                          'DIVX'), fps, (background.shape[1], background.shape[0]))

    for frame in final_video:
        #cv2.imshow('Video summary',frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    #     tm.sleep(1/30) #TODO: FPS
    out.release()
    cv2.destroyAllWindows()
    cap.release()

    print("Done!!")
    print("Summary video is available at " + filename + '_summary.avi')


