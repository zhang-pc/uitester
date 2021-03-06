# @Time    : 2016/11/18 16:32
from keywords import get_var, keyword, call


@keyword("click_id")
def click_id(view_id, index=0):
    solo = get_var("solo")
    # solo.sleep(3000)
    view = get_view(view_id, index)
    click_view(view)


@keyword("click_text")
def click_text(text):
    solo = get_var("solo")
    solo.click_on_text(text)


@keyword("click_view")
def click_view(view):
    solo = get_var("solo")
    solo.click_on_view(view)


@keyword("get_view")
def get_view(view_id, index=0):
    solo = get_var("solo")
    return solo.get_view(res_id=view_id, index=index)


@keyword("get_view_text")
def get_text(view_id, index=0):
    solo = get_var("solo")
    view = solo.get_view(res_id=view_id, index=index)
    return call(view, "getText")


@keyword("sleep")
def sleep(milliseconds):
    solo = get_var("solo")
    solo.sleep(milliseconds)


@keyword("wait_for_view")
def wait_for_text(class_name):
    solo = get_var("solo")
    return solo.wait_for_view(class_name)


@keyword("get_text_view_line_count")
def get_text_view_line_count(view):
    return call(view, "getLineCount")


@keyword("finish_app")
def finish_app():
    """
    finish app
    :return:
    """
    solo = get_var("solo")
    solo.finish_opened_activities()


@keyword("scroll_to_right")
def scroll_to_right():
    """
    scroll to right
    :return:
    """
    solo = get_var("solo")
    solo.scroll_to_right()


@keyword("scroll_to_left")
def scroll_to_left():
    """
    scroll to left
    :return:
    """
    solo = get_var("solo")
    solo.scroll_to_left()


@keyword("get_text_from_parent")
def get_text_from_parent(view, text, index=0):
    """
    获取父级view下的指定文本,返回TextView

    用法示例:
    get_text_from_parent parent_view text 1
    
    注：index不输入时，默认为0
    :param view:
    :param text:
    :param index:
    :return:
    """
    solo = get_var("solo")
    view = solo.get_text_from_parent(view, text, index)
    return view
