#!/usr/bin/env python3

import time, json, threading, subprocess, queue, platform, os
import numpy as np
from housepy import log, config, strings, net, s3, util, process
from scipy.io import wavfile

DURATION = 10
AUDIO_TMP = os.path.abspath(os.path.join(os.path.dirname(__file__), "audio_tmp"))

process.secure_pid(os.path.join(os.path.dirname(__file__), "run"))


class Recorder(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.out_queue = queue.Queue()
        self.start() 

    def run(self):
        while True:
            t = util.timestamp()
            log.info("record %s" % t)
            try:
                if platform.system() == "Darwin":                
                    command = "cp audio_tmp/test.wav audio_tmp/%s.wav" % t  # for testing
                    time.sleep(DURATION)
                else:
                    command = "/usr/bin/arecord -D plughw:1,0 -d %s -f S16_LE -c1 -r11025 -t wav %s/%s.wav" % (DURATION, AUDIO_TMP, t)  # 10s of mono 11k PCM
                log.info("%s" % command)
                subprocess.check_call(command, shell=True)    
            except Exception as e:
                log.error(log.exc(e))
                time.sleep(DURATION)
                continue
            log.info("--> ok, wrote audio_tmp/%s.wav" % t)
            self.out_queue.put(t)


class Processor(threading.Thread):

    def __init__(self, recorder_queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.in_queue = recorder_queue
        self.out_queue = queue.Queue()
        self.start()

    def run(self):
        while True:
            t = self.in_queue.get()
            self.process(t)

    def process(self, t):
        log.info("process %s" % t)        
        try:
            filename = "%s/%s.wav" % (AUDIO_TMP, t)
            sample_rate, signal = wavfile.read(filename)
            log.debug("samples %s" % len(signal))
            log.debug("sample_rate %s" % sample_rate)
            duration = float(len(signal)) / sample_rate
            log.debug("duration %ss" % strings.format_time(duration))
            if platform.system() == "Darwin":                            
                signal = signal[:, 0]    # enforce mono
            signal = (np.array(signal).astype('float') / (2**16 * 0.5))   # assuming 16-bit PCM, -1 - 1
            signal = abs(signal)    # magnitude
            # log.debug("found magnitude")
            content_samples = 0
            for sample in signal:
                if sample > config['noise_threshold']:
                    content_samples += 1
            total_content_time = float(content_samples) / sample_rate
            log.info("total_content_time %s" % total_content_time)
            if total_content_time > config['time_threshold']:
                log.info("--> adding to upload queue")
                self.out_queue.put((t, filename))
            elif platform.system() != "Darwin":                            
                log.info("--> deleting file")
                os.remove(filename)
        except Exception as e:
            log.error(log.exc(e))


class Uploader(threading.Thread):

    def __init__(self, processor_queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.in_queue = processor_queue
        self.start()

    def run(self):
        while True:
            t, filename = self.in_queue.get()
            self.upload(t, filename)

    def upload(self, t, filename):      
        log.info("upload %s" % filename)          
        try:
            s3.upload(filename)
            log.info("--> uploaded. Pinging server...")
            data = {'t': t}
            response = net.read("http://%s:%s" % (config['server']['host'], config['server']['port']), json.dumps(data).encode('utf-8'))
            log.info(response)
            if platform.system() != "Darwin":    
                log.info("--> deleting local file")                        
                os.remove(filename)
        except Exception as e:
            log.error(log.exc(e))




recorder = Recorder()
processor = Processor(recorder.out_queue)
uploader = Uploader(processor.out_queue)
while True:
    time.sleep(0.1)

