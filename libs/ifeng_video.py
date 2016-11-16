from keywords import keyword, RemoteObject, get_local_ip, call_static, set_var, get_var
from solo import InstrumentationRegistry, Solo

data_interface_class_name = "com.ifeng.at.testagent.reflect.DataInterfaceHelper"


@keyword("set_host")
def set_host():
    host = get_local_ip()
    data_interface = RemoteObject.from_class_name(data_interface_class_name)
    call_static(data_interface, "setHost", host)


@keyword("start_video")
def start_ifengvideo():
    instrumentation = InstrumentationRegistry.get_instrumentation()
    intent = instrumentation \
        .get_target_context() \
        .get_package_manager() \
        .get_launch_intent_for_package("com.ifeng.newvideo")
    activity = instrumentation.start_activity_sync(intent)
    solo = Solo(instrumentation, activity)
    set_var("solo", solo)


@keyword("wait")
def wait_debug(wait_time):
    import time
    time.sleep(int(wait_time))


@keyword("get_host")
def get_host():
    data_interface = RemoteObject.from_class_name("com.ifeng.video.dao.db.constants.DataInterface")
    v = data_interface.get_field("LIVE_CHANNEL_INFO")
    print(v)