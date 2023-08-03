"""
(*)~----------------------------------------------------------------------------------
 Pupil Helpers
 Copyright (C) 2012-2016  Pupil Labs

 Distributed under the terms of the GNU Lesser General Public License (LGPL v3.0).
 License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
"""

"""
This example demonstrates how to send annotations via Pupil Remote. 

In order to ensure accurate alignment of this script's local clock with Pupil Time, we
implement a simple real-time sync protocol. For more information, please see
'simple_realtime_time_sync.py'
"""

import zmq
import msgpack as serializer
import time
import socket
import sys


def main(id: str, ip_address: str = "127.0.0.1", port: int = 50020):
    """
    This example performs these steps:
    1. Setup network connection
    2. Setup "local" clock function
    3. Measure clock offset accounting for network latency variance
    4. Prepare and send annotations

    Parameters:
    ----------
    id (str) : name of the recofding.
    ip_address (str) : ip address to which the eyetracker is connected. By defualt
    it is set to 127.0.0.1. This assumes that the eyetracker is connected to this
    machine.
    
    port (int) : port. By defualt it is set to 50020. Don't change it unless
    you know what you are doing.
    """

    # 1. Setup network connection
    check_capture_exists(ip_address, port)
    pupil_remote, pub_socket = setup_pupil_remote_connection(ip_address, port)

    # 2. Setup local clock function
    local_clock = time.perf_counter

    # 3. Measure clock offset accounting for network latency
    stable_offset_mean = measure_clock_offset_stable(
        pupil_remote, clock_function=local_clock, n_samples=10
    )

    pupil_time_actual = request_pupil_time(pupil_remote)
    local_time_actual = local_clock()
    pupil_time_calculated_locally = local_time_actual + stable_offset_mean
    print(f"Pupil time actual: {pupil_time_actual}")
    print(f"Local time actual: {local_time_actual}")
    print(f"Stable offset: {stable_offset_mean}")
    print(f"Pupil time (calculated locally): {pupil_time_calculated_locally}")

    # 4. Prepare and send annotations
    # Start the annotations plugin
    notify(
        pupil_remote,
        {"subject": "start_plugin", "name": "Annotation_Capture", "args": {}},
    )

    # start a recording (necessary for this example script)
    pupil_remote.send_string(f"R {id}")
    pupil_remote.recv_string()
    time.sleep(1.0)  # sleep for a few seconds, can be less

    # Send an annotation.
    # We send a timestamp sampled from the local clock (e.g. that corresponds to a
    # trigger event, or a stimulus that was presented). The clock offset that we
    # measured in step 3 will be added to the timestamp to correctly align it with
    # Pupil Time. The annotation will be saved to annotation.pldata if a recording is
    # running. The Annotation_Player plugin will automatically retrieve, display and
    # export all recorded annotations.
    local_time = local_clock()
    label = "high price"
    minimal_trigger = new_trigger(label, local_time + stable_offset_mean)
    send_trigger(pub_socket, minimal_trigger)
    time.sleep(20.0)  # sleep for a few seconds, can be less

    # Send another trigger with the current time
    local_time = local_clock()
    label = 'low price'
    minimal_trigger = new_trigger(label, local_time + stable_offset_mean)
    send_trigger(pub_socket, minimal_trigger)

    # Add custom keys to your annotation
    minimal_trigger["custom_key"] = "x"
    send_trigger(pub_socket, minimal_trigger)
    time.sleep(20.0)  # sleep for a few seconds, can be less

    # stop recording
    pupil_remote.send_string("r")
    pupil_remote.recv_string()


def check_capture_exists(ip_address: str = '127.0.0.1' , port : int = 50020):
    """
    Check whether pupil capture instance exists. Returns True if the Pupil
    Capture was found. Otherwise returns False.
    
    Parameters:
    ----------
    ip_address (str) : ip address to which the eyetracker is connected. By defualt
    it is set to 127.0.0.1. This assumes that the eyetracker is connected to this
    machine.
    
    port (int) : port. By defualt it is set to 50020. Don't change it unless
    you know what you are doing.
    
    Returns:
    -------
    (bool) : Returns True if the Pupil Capture was found. Otherwise, it returns
    False.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if not sock.connect_ex((ip_address, port)):
            print("Found Pupil Capture")
            return True
        print("Cannot find Pupil Capture")
        return False


def setup_pupil_remote_connection(ip_address: str = '127.0.0.1', port: int = 50020) -> tuple:
    """
    Creates a zmq-REQ socket and connects it to Pupil Capture or Service
    to send and receive notifications.

    We also set up a PUB socket to send the annotations. This is necessary to write
    messages to the IPC Backbone other than notifications

    See https://docs.pupil-labs.com/developer/core/network-api/ for details.

    Parameters:
    ----------
    ip_address (str) : ip address to which the eyetracker is connected. By defualt
    it is set to 127.0.0.1. This assumes that the eyetracker is connected to this
    machine.
    
    port (int) : port. By defualt it is set to 50020. Don't change it unless
    you know what you are doing.

    Returns:
    -------
    (tuple) : zmq-REQ and PUB sockets to connect with Pupil Capture and to send 
    notifications.
    
    """
    # zmq-REQ socket
    ctx = zmq.Context.instance()
    pupil_remote = ctx.socket(zmq.REQ)
    pupil_remote.connect(f"tcp://{ip_address}:{port}")

    # PUB socket
    pupil_remote.send_string("PUB_PORT")
    pub_port = pupil_remote.recv_string()
    pub_socket = zmq.Socket(ctx, zmq.PUB)
    pub_socket.connect("tcp://127.0.0.1:{}".format(pub_port))

    return pupil_remote, pub_socket


def request_pupil_time(pupil_remote) -> float:
    """Uses an existing Pupil Core software connection to request the remote time.
    Returns the current "pupil time" at the timepoint of reception.
    See https://docs.pupil-labs.com/core/terminology/#pupil-time for more information
    about "pupil time".
    
    Parameters:
    ----------
    pupil_remote (zmq-REQ socket) : existing Pupil Core software connection.

    Returns:
    ------
    (float) : the current 'pupil time' at the timepoint of reception.
    """
    pupil_remote.send_string("t")
    pupil_time = pupil_remote.recv()
    return float(pupil_time)


def measure_clock_offset(pupil_remote, clock_function) -> float:
    """Calculates the offset between the Pupil Core software clock and a local clock.
    Requesting the remote pupil time takes time. This delay needs to be considered
    when calculating the clock offset. We measure the local time before (A) and
    after (B) the request and assume that the remote pupil time was measured at (A+B)/2,
    i.e. the midpoint between A and B.

    As a result, we have two measurements from two different clocks that were taken
    assumingly at the same point in time. The difference between them ("clock offset")
    allows us, given a new local clock measurement, to infer the corresponding time on
    the remote clock.

    Parameters:
    ----------
    pupil_remote (zmq-REQ socket) : existing Pupil Core software connection.
    clock_function (function) : a function that returns local time.
    

    Returns:
    ------
    (float) : a delay between local clock and pupil clock.
    """
    local_time_before = clock_function()
    pupil_time = request_pupil_time(pupil_remote)
    local_time_after = clock_function()

    local_time = (local_time_before + local_time_after) / 2.0
    clock_offset = pupil_time - local_time
    return clock_offset


def measure_clock_offset_stable(pupil_remote, clock_function, n_samples: int = 10) -> float:
    """
    Returns the mean clock offset after multiple measurements to reduce the effect
    of varying network delay.

    Since the network connection to Pupil Capture/Service is not necessarily stable,
    one has to assume that the delays to send and receive commands are not symmetrical
    and might vary. To reduce the possible clock-offset estimation error, this function
    repeats the measurement multiple times and returns the mean clock offset.

    The variance of these measurements is expected to be higher for remote connections
    (two different computers) than for local connections (script and Core software
    running on the same computer). You can easily extend this function to perform
    further statistical analysis on your clock-offset measurements to examine the
    accuracy of the time sync.

    Parameters:
    ----------
    pupil_remote (zmq-REQ socket) : existing Pupil Core software connection.
    clock_function (function) : a function that returns local time.
    n_sample (int) : a number of measurements. By default it is set to 10.
    It must be at least 1.
    

    Returns:
    ------
    (float) : a mean delay between local clock and pupil clock.
    """
    assert n_samples > 0, "Requires at least one sample"
    offsets = [
        measure_clock_offset(pupil_remote, clock_function) for x in range(n_samples)
    ]
    return sum(offsets) / len(offsets)  # mean offset


def notify(pupil_remote, notification) -> str:
    """
    Sends ``notification`` to Pupil Remote. It returns a string with
    the response from Pupil Remote.

    Parameters:
    ----------
    pupil_remote (zmq_REQ socket) : existing Pupil Core software connection.
    notification (dict) : the notification send to Pupil Remote.  

    Returns:
    -------
    (str) : the response from Pupil Remote.
    """
    topic = "notify." + notification["subject"]
    payload = serializer.dumps(notification, use_bin_type=True)
    pupil_remote.send_string(topic, flags=zmq.SNDMORE)
    pupil_remote.send(payload)
    return pupil_remote.recv_string()


def send_trigger(pub_socket, trigger) -> None:
    """
    Sends annotation via PUB port.

    Parameters:
    ----------
    pub_socket (PUB socket) : a socket to send annotations.
    trigger (dict) : an annotations to send.
    """
    payload = serializer.dumps(trigger, use_bin_type=True)
    pub_socket.send_string(trigger["topic"], flags=zmq.SNDMORE)
    pub_socket.send(payload)


def new_trigger(label, timestamp) -> dict:
    """
    Creates a new trigger/annotation to send to Pupil Capture.
    It returns a dictionary with annotation to send.
    
    Parameters:
    ----------
    label (str) : annotation label.
    timestamp (float) : timestamp of the annotation.

    Returns:
    (dict) : annotation to send to Pupil Capture.
    """
    return {
        "topic": "annotation",
        "label": label,
        "timestamp": timestamp,
    }


if __name__ == "__main__":
    main()
