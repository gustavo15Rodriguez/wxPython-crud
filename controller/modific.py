import wx
from wx import xrc
from controller.usercontroller import UserController

class ModificFrame(wx.Frame):

    def __init__(self, frame_father=None,id_user=None):
        super(ModificFrame, self).__init__()
        self.res = xrc.XmlResource('../view/modific.xrc')
        self.frame = self.res.LoadFrame(None, 'ModificFrame')
        self.panel = xrc.XRCCTRL(self.frame, 'InicioModific')
        self.user_controller = UserController()
        self.id_user = id_user
        self.first_name = xrc.XRCCTRL(self.panel, 'textModFirstName')
        self.last_name = xrc.XRCCTRL(self.panel, 'textModLastName')
        self.username = xrc.XRCCTRL(self.panel, 'textModUsername')
        self.password = xrc.XRCCTRL(self.panel, 'textModPassword')
        self.button_save = xrc.XRCCTRL(self.panel, 'wxID_OK')
        self.button_cancel = xrc.XRCCTRL(self.panel, 'wxID_CANCEL')
        self.frame.Bind(wx.EVT_BUTTON, self.close_frame, self.button_cancel)
        self.frame.Bind(wx.EVT_BUTTON, self.update_user, self.button_save)
        self.frame.Show()

        if frame_father is not None:
            self.frame_father = frame_father

        if self.id_user is not None:
            self.load_data_user()

    def update_user(self, evt):
        first_name = self.first_name.GetValue()
        last_name = self.last_name.GetValue()
        username = self.username.GetValue()
        password = self.password.GetValue()

        if first_name and last_name and username and password:

            if self.id_user is not None:
                data = {'first_name': first_name, 'last_name': last_name, 'username': username, 'password': password}
                self.user_controller.edit_user(self.id_user, data)
                wx.MessageBox('The user has been update successfully', 'Information', wx.OK | wx.ICON_INFORMATION)
                self.load_data_user()

            else:
                self.user_controller.create_user(first_name, last_name, username, password)

            self.frame_father.load_data_listctrl_user()

        else:
            wx.MessageBox('Fields not entered', 'Error', wx.OK | wx.ICON_ERROR)

        self.frame_father.load_data_listctrl_user()


    def close_frame(self, evt):
        self.frame.Close()

    def load_data_user(self):
        user = self.user_controller.get_user(self.id_user)
        self.first_name.SetValue(user.first_name)
        self.last_name.SetValue(user.last_name)
        self.username.SetValue(user.username)
        self.password.SetValue(user.password)


if __name__ == '__main__':
    app = wx.App()
    frame = ModificFrame()
    app.MainLoop()
