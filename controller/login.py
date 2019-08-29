import wx
from wx import xrc
from controller.usercontroller import UserController
from controller.inicio import InicioFrame
from controller.register import RegistroFrame
from controller.inicio_user import InicioUser

class LoginFrame(wx.Frame):

    def __init__(self):
        super(LoginFrame, self).__init__()
        self.res = xrc.XmlResource('../view/login.xrc')
        self.user_controller = UserController()
        self.main_menu = None
        self.inicio_user = None
        self.frame = self.res.LoadFrame(None, 'LoginFrame')
        self.panel = xrc.XRCCTRL(self.frame, 'InicioPanel')
        self.username = xrc.XRCCTRL(self.frame, 'text_user')
        self.password = xrc.XRCCTRL(self.frame, 'text_pass')
        self.button = xrc.XRCCTRL(self.panel, 'sign_in')
        self.frame.Bind(wx.EVT_BUTTON, self.validate_user, self.button)
        self.open = xrc.XRCCTRL(self.panel, 'account')
        self.frame.Bind(wx.EVT_BUTTON, self.open_register, self.open)
        self.frame.Show()

    def open_register(self, evt):
        self.register = RegistroFrame()

    def validate_user(self, evt):
        username = self.username.GetValue()
        password = self.password.GetValue()

        if username and password:
            if self.user_controller.search_user(username, password):
                if username == '@gustavo15' and password == 'gustavo12345':
                    self.frame.Close()
                    self.main_menu = InicioFrame()

                else:
                    self.frame.Close()
                    user = self.user_controller.search_username(username)
                    if user is not False:
                        self.inicio_user = InicioUser(user=user, frame_father=self)

                    else:
                        wx.MessageBox('User is not valid', 'Error', wx.OK | wx.ICON_INFORMATION)

            else:
                wx.MessageBox('User does not exist', 'Error', wx.OK | wx.ICON_ERROR)

        else:
            wx.MessageBox('Fields not entered', 'Error', wx.OK | wx.ICON_ERROR)

if __name__== '__main__':
    app = wx.App()
    frame = LoginFrame()
    app.MainLoop()
