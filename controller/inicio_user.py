import wx
from wx import xrc
from controller.usercontroller import UserController
from controller.series import Series
from controller.videogames import VideoGame
from controller.vista_serie_users import VistaUserSerie
from controller.vista_game_user import VistaGameUser
from controller.conection import Conection
from model.model import Serie, Videojuego
from sqlalchemy.orm.exc import MultipleResultsFound


class InicioUser(wx.Frame):

    def __init__(self, user=None, frame_father=None):
        super(InicioUser, self).__init__()
        self.res = xrc.XmlResource('../view/inicio_user.xrc')
        self.frame = self.res.LoadFrame(None, 'InicioUser')
        self.panel = xrc.XRCCTRL(self.frame, 'InicioPanel')

        self.user_controller = UserController()
        self.user = user
        self.series = Series()
        self.games = VideoGame()
        self.conect = Conection()
        self.frame_father = frame_father

        #User
        self.listbook_user = xrc.XRCCTRL(self.panel, 'listbook')
        self.panel_user = xrc.XRCCTRL(self.listbook_user, 'panel2')
        self.button = xrc.XRCCTRL(self.panel_user, 'log_out')
        self.frame.Bind(wx.EVT_BUTTON, self.close_frames, self.button)

        self.welcome = xrc.XRCCTRL(self.listbook_user, 'staticTextHi')
        self.firstname = xrc.XRCCTRL(self.listbook_user, 'textCtrlName')
        self.lastname = xrc.XRCCTRL(self.listbook_user, 'textCtrlLastName')
        self.username = xrc.XRCCTRL(self.listbook_user, 'textCtrlUsername')
        self.password = xrc.XRCCTRL(self.listbook_user, 'textCtrlPassword')

        self.button_modificate = xrc.XRCCTRL(self.listbook_user, 'buttonModificate')
        self.frame.Bind(wx.EVT_BUTTON, self.modific_user, self.button_modificate)

        self.button_eliminate = xrc.XRCCTRL(self.listbook_user, 'buttonEliminate')
        self.frame.Bind(wx.EVT_BUTTON, self.eliminate_user, self.button_eliminate)

        #Series
        self.listbook_menu = xrc.XRCCTRL(self.panel, 'panelSerie')
        self.text_search_serie = xrc.XRCCTRL(self.listbook_menu, 'textCtrlSerie')
        self.button_search = xrc.XRCCTRL(self.listbook_menu, 'searchSerie')
        self.frame.Bind(wx.EVT_BUTTON, self.search_serie, self.button_search)
        self.grid_serie = xrc.XRCCTRL(self.listbook_menu, 'scrolledWindowSerie')
        self.button_exit_serie = xrc.XRCCTRL(self.listbook_menu, 'exit')
        self.frame.Bind(wx.EVT_BUTTON, self.close_frames, self.button_exit_serie)
        self.grid_sizer_series()

        #Videojuegos
        self.listbook_games = xrc.XRCCTRL(self.panel, 'panelGames')
        self.text_search_game = xrc.XRCCTRL(self.listbook_games, 'textCtrlGame')
        self.button_search_game = xrc.XRCCTRL(self.listbook_games, 'searchGame')
        self.frame.Bind(wx.EVT_BUTTON, self.search_game, self.button_search_game)
        self.grid_game = xrc.XRCCTRL(self.listbook_games, 'scrolledWindowGame')
        self.button_exit_games = xrc.XRCCTRL(self.listbook_games, 'logOut')
        self.frame.Bind(wx.EVT_BUTTON, self.close_frames, self.button_exit_games)
        self.grid_sizer_games()

        self.load_data_user()
        self.load_welcome()

        self.frame.Show()

    def search_serie(self, evt):
        text_serie = str(self.text_search_serie.GetValue())
        session = self.conect.connect_database()

        try:
            serie = session.query(Serie).filter_by(titulo_serie=text_serie).all()
            if text_serie != "":
                if serie:

                    wx.MessageBox('The serie exist in this aplication')

                else:
                    wx.MessageBox('The serie does not exist in this aplication')

            else:
                wx.MessageBox('Fields no entered')

            session.close()

        except MultipleResultsFound:
            session.close()
            return False

    def search_game(self, evt):
        text_game = str(self.text_search_game.GetValue())
        session = self.conect.connect_database()

        try:
            game = session.query(Videojuego).filter_by(titulo_videojuego=text_game).all()
            if text_game != "":
                if game:
                    wx.MessageBox('The videogame exist in this aplication.')

                else:
                    wx.MessageBox('The videogame does not exist in this aplication.')

            else:
                wx.MessageBox('Fields no entered')

            session.close()

        except MultipleResultsFound:
            session.close()
            return False

    def load_welcome(self):
        first_name = self.firstname.GetValue()
        load = self.user_controller.get_first_name_user(first_name)
        cont = 0
        if load is None:
            cont+=1

        if cont >1:
            new = self.user_controller.get_first_name_user(self.user.first_name)
            self.welcome.SetLabel('Welcome, %s!!!'%new)

        else:
            self.welcome.SetLabel('Welcome, %s!!!' % load)

    def modific_user(self, evt):
        first_name = self.firstname.GetValue()
        last_name = self.lastname.GetValue()
        username = self.username.GetValue()
        password = self.password.GetValue()

        if first_name and last_name and username and password:

            if self.user.id is not None:
                data = {'first_name': first_name, 'last_name': last_name, 'username': username, 'password': password}
                self.user_controller.edit_user(self.user.id, data)
                wx.MessageBox('The user has been update successfully', 'Information', wx.OK | wx.ICON_INFORMATION)
                self.load_welcome()

        else:
            wx.MessageBox('Fields not entered', 'Error', wx.OK | wx.ICON_ERROR)

    def load_data_user(self):
        user = self.user_controller.search_username(username=self.user.username)
        self.firstname.SetValue(user.first_name)
        self.lastname.SetValue(user.last_name)
        self.username.SetValue(user.username)
        self.password.SetValue(user.password)

    def eliminate_user(self, evt):
        msg = "Is you sure to delete your user?"
        result = wx.MessageBox(msg, "Delete user", wx.YES_NO | wx.ICON_EXCLAMATION)

        if result == wx.YES:
            self.user_controller.delete_user(self.user.id)
            wx.MessageBox("The user has been eliminated successfully!")
            self.frame.Close()

    def close_frames(self, evt):
        self.frame.Close()

    def grid_sizer_games(self):
        cols = 2
        images_games = self.games.get_all_images_games()
        cantidad = len(images_games)
        filas = cantidad // cols

        if cantidad % cols != 0:
            filas += 1

        grid_sizer = wx.GridSizer(filas, cols, 5, 5)
        indicador = 0
        for i in range(grid_sizer.GetRows()):
            for j in range(grid_sizer.GetCols()):
                if indicador < len(images_games):
                    button = wx.BitmapButton(self.grid_game, name=str(images_games[indicador].id), bitmap=wx.Bitmap(images_games[indicador].imagen_url))
                    grid_sizer.Add(button, 0, wx.EXPAND)
                    self.grid_game.Bind(wx.EVT_BUTTON, self.click_images_game, button)
                    self.grid_game.SetSizer(grid_sizer)
                    indicador += 1

    def grid_sizer_series(self):
        cols = 2
        images_series = self.series.get_all_images()
        cantidad = len(images_series)
        filas = cantidad // cols

        if cantidad % cols != 0:
            filas += 1

        grid_sizer = wx.GridSizer(filas, cols, 5, 5)
        indicador = 0
        for i in range(grid_sizer.GetRows()):
            for j in range(grid_sizer.GetCols()):
                if indicador < len(images_series):
                    button = wx.BitmapButton(self.grid_serie, name=str(images_series[indicador].id), bitmap=wx.Bitmap(images_series[indicador].imagen_url))
                    grid_sizer.Add(button, 0, wx.EXPAND)
                    self.grid_serie.Bind(wx.EVT_BUTTON, self.click_images_serie, button)
                    self.grid_serie.SetSizer(grid_sizer)
                    indicador += 1

    def click_images_serie(self, evt):
        id_serie = evt.GetEventObject().GetName()
        VistaUserSerie(id_serie=id_serie, id_user=self.user.id)

    def click_images_game(self, evt):
        id_game = evt.GetEventObject().GetName()
        VistaGameUser(id_game=id_game, id_user=self.user.id)

if __name__ == '__main__':
    app = wx.App()
    frame = InicioUser()
    app.MainLoop()