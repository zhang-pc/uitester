# # @Time    : 2016/11/17 14:52
# # @Author  : lixintong
# from keywords import keyword, get_var, call
# # from player import get_view_by_id, click_view, tabs_id, click_main_tab
#
login_et_account_id = "com.ifeng.newvideo:id/login_et_account"
login_et_pwd_id = "com.ifeng.newvideo:id/login_et_pwd"
login_btn_id = "com.ifeng.newvideo:id/tv_login_btn"
# login_name = "com.ifeng.newvideo:id/tv_login"
# login_out_id = "com.ifeng.newvideo:id/setting_login_out"
login_back = "com.ifeng.newvideo:id/back"
#
#
from keywords import get_var, keyword


@keyword("login_in")
def login_et(account, pwd):
    solo = get_var("solo")
    et_account_view = solo.get_view(login_et_account_id)
    et_pwd_view = solo.get_view(login_et_pwd_id)
    solo.clear_edit_text(et_account_view)
    solo.enter_text(et_account_view, account)
    solo.enter_text(et_pwd_view, pwd)
    login_btn = solo.get_view(login_btn_id)
    solo.click_on_view(login_btn)


# @keyword("exit_login")
# def exit_login():
#     solo = get_var("solo")
#     solo.sleep(1000)
#     click_main_tab("我的")
#     view = solo.get_view(login_name)
#     text = call(view, "getText")
#     if text == "登录":
#         pass
#     else:
#         solo.click_on_view(view)
#         solo.sleep(1000)
#         login_out_view = solo.get_view(login_out_id)
#         solo.click_on_view(login_out_view)
#         solo.sleep(1000)
#         solo.click_on_text("确定")
#
#
# @keyword("click_login_back")
# def click_login_back():
#     click_view(login_back)
#
# # @keyword("check_login_state")
# # def check_login_state(expect_result):
# #     expect_result = change_to_bool(expect_result)
