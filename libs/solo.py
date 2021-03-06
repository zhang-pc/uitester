from keywords import keyword, new, call, call_static, RemoteObject

instrument_registry = 'android.support.test.InstrumentationRegistry'
instrumentation_class_name = 'android.app.Instrumentation'
solo_class_name = 'com.robotium.solo.Solo'
android_view = 'android.view.View'
android_edit_text = 'android.widget.EditText'
java_float = 'java.lang.Float'
java_object = 'java.lang.Object'
activity_class_name = 'android.app.Activity'
ui_device_class_name = 'android.support.test.uiautomator.UiDevice'


class Intent(RemoteObject):
    FLAG_ACTIVITY_NEW_TASK = 0x10000000

    def add_flags(self, flag):
        call(self, 'addFlags', flag)


class Context(RemoteObject):
    def get_package_manager(self):
        obj = call(self, 'getPackageManager')
        return PackageManager.from_object(obj)

    def start_activity(self, intent):
        call(self, 'startActivity', intent)


class Activity(RemoteObject):
    pass


class PackageManager(RemoteObject):
    def get_launch_intent_for_package(self, package_name):
        obj = call(self, 'getLaunchIntentForPackage', package_name)
        return Intent.from_object(obj)


class Instrumentation(RemoteObject):
    def start_activity_sync(self, intent):
        obj = call(self, 'startActivitySync', intent)
        return Activity.from_object(obj)

    def get_context(self):
        obj = call(self, 'getContext')
        return Context.from_object(obj)

    def get_target_context(self):
        obj = call(self, 'getTargetContext')
        return Context.from_object(obj)


class InstrumentationRegistry(RemoteObject):
    @staticmethod
    def get_instrumentation():
        instrument_registry_class = RemoteObject.from_class_name(instrument_registry)
        remote_obj = call_static(instrument_registry_class, "getInstrumentation")
        return Instrumentation.from_object(remote_obj)


class Solo(RemoteObject):
    def __init__(self, instrumentation, activity=None):
        super().__init__()
        solo_class = RemoteObject.from_class_name(solo_class_name)
        instrumentation.class_name = instrumentation_class_name
        if activity:
            activity.class_name = activity_class_name
            remote_solo = new(solo_class, instrumentation, activity)
        else:
            remote_solo = new(solo_class, instrumentation)
        self.__dict__.update(remote_solo.__dict__)

    def get_view(self, res_id=None, class_name=None, index=None):
        if res_id:
            if index:
                return call(self, "getView", res_id, index)
            return call(self, "getView", res_id)
        if class_name:
            if index:
                return call(self, "getView", RemoteObject.from_class_name(class_name), index)
            return call(self, "getView", RemoteObject.from_class_name(class_name))

    def wait_for_text(self, text):
        """
        Waits for the specified text to appear. Default timeout is 20 seconds.
        @param text the text to wait for, specified as a regular expression
        @return {@code true} if text is displayed and {@code false} if it is not displayed before the timeout
        """
        return call(self, "waitForText", text)

    def wait_for_view(self, class_name):
        """
        Waits for a View matching the specified class. Default timeout is 20 seconds.
        :param class_name:viewClass the {@link View} class to wait for
        :return:{@code true} if the {@link View} is displayed and {@code false} if it is not displayed before the timeout
        """

        return call(self, "waitForView", RemoteObject.from_class_name(class_name))

    def get_current_activity(self):
        """
        Returns the current Activity.
        :return: the current Activity.
        """
        obj = call(self, "getCurrentActivity")
        return Activity.from_object(obj)

    def assert_memory_not_low(self):
        """
        Asserts that the available memory is not considered low by the system.
        """
        return call(self, "assertMemoryNotLow")

    def wait_for_dialog_to_open(self):
        """
        Waits for a Dialog to open. Default timeout is 20 seconds.
        :return: {@code true} if the {@link android.app.Dialog} is opened before the timeout and {@code false} if it is not opened
        """
        return call(self, "waitForDialogToOpen")

    def wait_for_dialog_to_close(self):
        """
        Waits for a Dialog to close. Default timeout is 20 seconds.
        :return: @return {@code true} if the {@link android.app.Dialog} is closed before the timeout and {@code false} if it is not closed
        """
        return call(self, "waitForDialogToClose")

    def go_back(self):
        """
        Simulates pressing the hardware back key.
        """
        return call(self, "goBack")

    def click_on_screen(self, x, y):
        """
        Clicks the specified coordinates.
        :param x: the x coordinate
        :param y: the y coordinate
        """
        return call(self, "clickOnScreen", RemoteObject.from_float(x), RemoteObject.from_float(y))

    def click_long_on_screen(self, x, y):
        """
        Long clicks the specified coordinates.
        :param x: the x coordinate
        :param y: the y coordinate
        """
        return call(self, "clickLongOnScreen", RemoteObject.from_float(x), RemoteObject.from_float(y))

    def click_on_button(self, text):
        """
        Clicks a Button displaying the specified text. Will automatically scroll when needed.
        :param text: the text displayed by the {@link Button}. The parameter will be interpreted as a regular expression
        """
        return call(self, "clickOnButton", text)

    def click_on_image_button(self, index):
        """
        Clicks an ImageButton matching the specified index.
        :param index: the index of the {@link ImageButton} to click. 0 if only one is available
        """
        return call(self, "clickOnImageButton", index)

    def click_on_toggle_button(self, text):
        """
        Clicks a ToggleButton displaying the specified text.
        :param text: the text displayed by the {@link ToggleButton}. The parameter will be interpreted as a regular expression
        """
        return call(self, "clickOnToggleButton", text)

    def click_on_view(self, view):
        """
        Clicks the specified View.
        :param view: the {@link View} to click
        :return:
        """
        view.class_name = android_view
        return call(self, "clickOnView", view)

    def click_long_on_view(self, view):
        """
        Long clicks the specified View.
        :param view: the {@link View} to long click
        :return:
        """
        view.class_name = android_view
        return call(self, "clickLongOnView", view)

    def click_on_text(self, text):
        """
        Clicks a View or WebElement displaying the specified
        text. Will automatically scroll when needed.
        :param text: the text to click. The parameter will be interpreted as a regular expression
        """
        return call(self, "clickOnText", text)

    def click_long_on_text(self, text):
        """
        Long clicks a View or WebElement displaying the specified text. Will automatically scroll when needed.
        :param text: the text to click. The parameter will be interpreted as a regular expression
        """
        return call(self, "clickLongOnText", text)

    def drag(self, from_x, to_x, from_y, to_y, step_count):
        """
        Simulate touching the specified location and dragging it to a new location.


        :param from_x : x coordinate of the initial touch, in screen coordinates
        :param to_x : x coordinate of the drag destination, in screen coordinates
        :param from_y : y coordinate of the initial touch, in screen coordinates
        :param to_y : y coordinate of the drag destination, in screen coordinates
        :param step_count : how many move steps to include in the drag. Less steps results in a faster drag
        """
        return call(self, "drag", RemoteObject.from_float(from_x), RemoteObject.from_float(to_x),
                    RemoteObject.from_float(from_y), RemoteObject.from_float(to_y), step_count)

    def enter_text(self, edit_text_view, text):
        """
        Enters text in the specified EditText.
        :param edit_text_view: the {@link EditText} to enter text in
        :param text: the text to enter in the {@link EditText} field
        """
        edit_text_view.class_name = android_edit_text
        return call(self, "enterText", edit_text_view, text)

    def clear_edit_text(self, edit_text_view):
        """
        Clears the value of an EditText.
        :param edit_text_view: the {@link EditText} to clear
        """
        edit_text_view.class_name = android_edit_text
        return call(self, "clearEditText", edit_text_view)

    def get_text(self, text):
        """
        Returns a TextView displaying the specified text.
        :param text: the text that is displayed, specified as a regular expression
        :return: the {@link TextView} displaying the specified text
        """
        return call(self, "getText", text)

    def get_button(self, text):
        """
        Returns a Button displaying the specified text.
        :param text: the text that is displayed, specified as a regular expression
        :return: the {@link Button} displaying the specified text
        """
        return call(self, "getButton", text)

    def hide_soft_keyboard(self):
        """
        Hides the soft keyboard.
        """
        return call(self, "hideSoftKeyboard")

    def unlock_screen(self):
        """
        Unlocks the lock screen.
        """
        return call(self, "unlockScreen")

    def wait_for_activity(self, name):
        """
        Waits for an Activity matching the specified name. Default timeout is 20 seconds.
        :param name: the name of the {@code Activity} to wait for. Example is: {@code "MyActivity"}
        :return: {@code true} if {@code Activity} appears before the timeout and {@code false} if it does not
        """
        return call(self, "waitForActivity", name)

    def wait_for_fragment_by_tag(self, tag):
        """
        Waits for a Fragment matching the specified tag.
        :param tag: the name of the tag
        :return {@code true}: if fragment appears and {@code false} if it does not appear before the timeout
        """
        return call(self, " waitForFragmentByTag", tag)

    def wait_for_log_message(self, message):
        """
        Waits for the specified log message to appear. Default timeout is 20 seconds.
        Requires read logs permission (android.permission.READ_LOGS) in AndroidManifest.xml of the application under test.
        :param message: the log message to wait for
        :return: {@code true} if log message appears and {@code false} if it does not appear before the timeout
        """
        return call(self, "waitForLogMessage", message)

    def clear_log(self):
        """
        Clears the log.
        """
        return call(self, "clearLog")

    def sleep(self, time):
        """
        Robotium will sleep for the specified time.
        :param time: the time in milliseconds that Robotium should sleep
        """
        return call(self, "sleep", time)

    def finalize(self):
        """
        Finalizes the Solo object and removes the ActivityMonitor.
        :see finishOpenedActivities(): finishOpenedActivities() to close the activities that have been active
        """
        return call(self, "finalize")

    def finish_opened_activities(self):
        """
        The Activities that are alive are finished. Usually used in tearDown().
        """
        return call(self, "finishOpenedActivities")

    def take_screenshot(self, name):
        """
        Takes a screenshot and saves it with the specified name in the {@link Config} objects save path (default set to: /sdcard/Robotium-Screenshots/).
        Requires write permission (android.permission.WRITE_EXTERNAL_STORAGE) in AndroidManifest.xml of the application under test.
        :param name: the name to give the screenshot
        """
        call(self, "takeScreenshot", name)

    def scroll_to_right(self):
        call(self, "scrollToSide", 22)

    def scroll_to_left(self):
        call(self, "scrollToSide", 21)

    def scroll_view_to_right(self, view):
        view.class_name = android_view
        call(self, "scrollViewToSide", view, 22)

    def scroll_view_to_left(self, view):
        view.class_name = android_view
        call(self, "scrollViewToSide", view, 21)

    def set_progress_bar(self, index, progress):
        """
        Sets the progress of a ProgressBar matching the specified index. Examples of ProgressBars are: {@link android.widget.SeekBar} and {@link android.widget.RatingBar}.
        :param index: the index of the {@link ProgressBar}
        :param progress: the progress to set the {@link ProgressBar}
        """
        call(self, "setProgressBar", index, progress)

    def drag_in_view(self, view, start_x, start_y, end_x, end_y, step_count):
        """
        Drag in view rect.
        :param start_x: start position on x, input percent value. e.g. 40 --> 40%
        :param start_y:
        :param end_x:
        :param end_y:
        :param step_count:
        :return:
        """
        view.class_name = android_view
        call(self, "dragInView", view, start_x, start_y, end_x, end_y, step_count)

    def get_text_from_parent(self, parent, text, index):
        """
        get TextView from parent view's children by text
        :param parent:
        :param text:
        :param index:
        :return:
        """
        parent.class_name = android_view
        return call(self, "getTextFromParent", parent, text, index)

    def get_view_from_parent(self, parent, res_id, index):
        """
        get View from parent view's children by view id string
        :param parent:
        :param res_id:
        :param index:
        :return:
        """
        parent.class_name = android_view
        return call(self, "getViewFromParent", parent, res_id, index)

    def get_displayed_views(self, res_id):
        """
        get views in window rect by view id str
        :param res_id:
        :return:
        """
        return call(self, "getDisplayedViews", res_id)

    def set_activity_orientation(self, orientation):
        """
        Sets the Orientation (Landscape/Portrait) for the current Activity.
        :param orientation: the orientation to set. <code>Solo.</code>{@link #LANDSCAPE} for landscape or <code>Solo.</code>{@link #PORTRAIT} for portrait.
        :return:
        """
        return call(self, "setActivityOrientation", orientation)


class UIDevice(RemoteObject):
    @classmethod
    def get_instance(cls, instrumentation):
        instrumentation.class_name = instrumentation_class_name
        ui_device_class = RemoteObject.from_class_name(ui_device_class_name)
        return UIDevice.from_object(call_static(ui_device_class, "getInstance", instrumentation))

    def press_home(self):
        call(self, "pressHome")

    def press_menu(self):
        """
        Simulates a short press on the MENU button.
        :return:
        """
        call(self, "pressMenu")

    def press_recent_apps(self):
        """
        Simulates a short press on the Recent Apps button.
        :return:
        """
        call(self, "pressRecentApps")

    def press_back(self):
        """
        Simulates a short press on the BACK button.
        :return:
        """
        call(self, "pressBack")


@keyword("runReflection")
def run_reflection_test():
    """
    Keywords test
    :return:
    """
    instrumentation = InstrumentationRegistry.get_instrumentation()
    intent = instrumentation \
        .get_context() \
        .get_package_manager() \
        .get_launch_intent_for_package("com.ifeng.at.testagent")
    activity = instrumentation.start_activity_sync(intent)
    print(activity.class_name)
    solo = Solo(InstrumentationRegistry.get_instrumentation())
    v = solo.get_view(res_id="com.ifeng.at.testagent:id/email_sign_in_button")
    print(v.class_name)
    solo.click_long_on_view(v)
    solo.sleep(5)
