import wx
from wx import xrc
from controller.usercontroller import UserController

class RegistroFrame(wx.Frame):

    def __init__(self, frame_father=None, id_user=None):
        super(RegistroFrame, self).__init__()
        self.res = xrc.XmlResource('../view/registro.xrc')
        self.user_controller = UserController()
        self.id_user = id_user
        self.frame = self.res.LoadFrame(None, 'RegistroFrame')
        self.panel = xrc.XRCCTRL(self.frame, 'InicioRegistro')
        self.first_name = xrc.XRCCTRL(self.panel, 'textCtrlFirstName')
        self.last_name = xrc.XRCCTRL(self.panel, 'textCtrlLastname')
        self.username = xrc.XRCCTRL(self.panel, 'textCtrlUsername')
        self.password = xrc.XRCCTRL(self.panel, 'textCtrlPassword')
        self.button_save = xrc.XRCCTRL(self.panel, 'wxID_OK')
        self.button_cancel = xrc.XRCCTRL(self.panel, 'wxID_CANCEL')

        self.frame.Bind(wx.EVT_BUTTON, self.close_frame, self.button_cancel)
        self.frame.Bind(wx.EVT_BUTTON, self.create_user, self.button_save)

        self.frame_father = frame_father

        if self.id_user is not None:
            self.load_data_user()

        self.frame.Show()

    def close_frame(self, evt):
        self.frame.Close()

    def create_user(self, evt):
        first_name = self.first_name.GetValue()
        last_name = self.last_name.GetValue()
        username = self.username.GetValue()
        password = self.password.GetValue()

        search_data = self.user_controller.search_username(username)

        if first_name and last_name and username and password:

            if self.id_user is not None:
                data = {'first_name': first_name, 'last_name': last_name, 'username': username, 'password': password}
                self.user_controller.edit_user(self.id_user, data)
                self.load_data_user()

            else:
                if search_data is None:
                    self.user_controller.create_user(first_name, last_name, username, password)
                    wx.MessageBox('The user has been created successfully', 'Information', wx.OK | wx.ICON_INFORMATION)
                    self.clear_fields()


                else:
                    wx.MessageBox('The username already exist in the database.', 'Error', wx.OK | wx.ICON_ERROR)

            if not self.frame_father is None:
                self.frame_father.load_data_listctrl_user()

        else:
            wx.MessageBox('Fields not entered', 'Error', wx.OK | wx.ICON_ERROR)

    def clear_fields(self):
        self.first_name.Clear()
        self.last_name.Clear()
        self.username.Clear()
        self.password.Clear()

    def load_data_user(self):
        user = self.user_controller.get_user(self.id_user)
        self.first_name.SetValue(user.first_name)
        self.last_name.SetValue(user.last_name)
        self.username.SetValue(user.username)
        self.password.SetValue(user.password)

if __name__== '__main__':
    app = wx.App()
    frame = RegistroFrame()
    app.MainLoop()
