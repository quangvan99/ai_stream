import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst

class Stream:
    def is_active(self) -> bool:
        pass
    
    def cb_newpad(self, decodebin, pad, source_id):
        print("In cb_newpad\n")
        caps = pad.get_current_caps()
        gststruct = caps.get_structure(0)
        gstname = gststruct.get_name()

        if gstname.find("video") != -1:
            pad_name = "sink_%u" % source_id
            sm = self.get_element("sm")
            sinkpad = sm.get_static_pad(pad_name)
            if sinkpad:
                print(f"Pad '{pad_name}' exists")
            else:
                print(f"Pad '{pad_name}' doesn't exist")
                sinkpad = sm.get_request_pad(pad_name)
            
            if sinkpad and pad.link(sinkpad) == Gst.PadLinkReturn.OK:
                print("Decodebin linked to pipeline successfully")
            else:
                print("Failed to link decodebin to pipeline")
                exit()

    def decodebin_child_added(self, child_proxy, Object, name, user_data):
        # Connect callback to internal decodebin signal
        if name.find("decodebin") != -1:
            Object.connect("child-added", self.decodebin_child_added, user_data)

        if "source" in name:
            source_element = child_proxy.get_by_name("source")
            if source_element.find_property('drop-on-latency') is not None:
                Object.set_property("drop-on-latency", True)
    

    def create_source_bin(self, index, uri):
        bin_name = f'src_{index}'
        uri_decode_bin=Gst.ElementFactory.make("uridecodebin", bin_name)
        if not uri_decode_bin:
            print(" Unable to create uri decode bin \n")
            exit()
        uri_decode_bin.set_property("uri",uri)
        uri_decode_bin.connect("pad-added", self.cb_newpad, index)
        uri_decode_bin.connect("child-added",self.decodebin_child_added, None)
        return uri_decode_bin