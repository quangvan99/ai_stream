from .base import *
from .stream import Stream
import sys

class Pipeline(Stream, BasePipeline):
    def __init__(self) -> None:
        pass

    def is_active(self) -> bool:
        pass

    def start(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def release(self) -> None:
        pass

    def run(self) -> None:
        pass

    def add_source(self, source_id, uri):
        #Create a uridecode bin with the chosen source id
        source_bin = self.create_source_bin(source_id, uri)

        if (not source_bin):
            sys.stderr.write("Failed to create source bin. Exiting.")
            exit(1)
        
        #Add source bin to our list and to pipeline
        self.pipeline.add(source_bin)

        #Set state of source bin to playing
        state_return = source_bin.set_state(Gst.State.PLAYING)

        if state_return == Gst.StateChangeReturn.SUCCESS:
            print("STATE CHANGE SUCCESS\n")

        elif state_return == Gst.StateChangeReturn.FAILURE:
            print("STATE CHANGE FAILURE\n")
        
        elif state_return == Gst.StateChangeReturn.ASYNC:
            state_return = source_bin.get_state(Gst.CLOCK_TIME_NONE)

        elif state_return == Gst.StateChangeReturn.NO_PREROLL:
            print("STATE CHANGE NO PREROLL\n")

        self.n_sources += 1
        self.perf_data = PERF_DATA(self.n_sources)
        

    def delete_source(self, source_id):
        print("Deleting source ", source_id)
        src = self.get_element(f"src_{source_id}")
        sm = self.get_element("sm")
        state_return = src.set_state(Gst.State.NULL)

        if state_return == Gst.StateChangeReturn.SUCCESS:
            print("STATE CHANGE SUCCESS\n")
            pad_name = "sink_%u" % source_id
            #Retrieve sink pad to be released
            sinkpad = sm.get_static_pad(pad_name)
            #Send flush stop event to the sink pad, then release from the streammux
            sinkpad.send_event(Gst.Event.new_flush_stop(False))
            sm.release_request_pad(sinkpad)
            print("STATE CHANGE SUCCESS\n",pad_name)
            #Remove the source bin from the pipeline
            self.pipeline.remove(src)

        elif state_return == Gst.StateChangeReturn.FAILURE:
            print("STATE CHANGE FAILURE\n")
        
        elif state_return == Gst.StateChangeReturn.ASYNC:
            state_return = src.get_state(Gst.CLOCK_TIME_NONE)
            pad_name = "sink_%u" % source_id
            sinkpad = sm.get_static_pad(pad_name)
            sinkpad.send_event(Gst.Event.new_flush_stop(False))
            sm.release_request_pad(sinkpad)
            
            print("STATE CHANGE ASYNC\n",pad_name)
            self.pipeline.remove(src)   

        self.n_sources -= 1
        del self.perf_data.all_stream_fps[f"stream{source_id}"]

    def change_source(self, source_id, uri):
        self.delete_source(source_id)
        self.add_source(source_id, uri) 