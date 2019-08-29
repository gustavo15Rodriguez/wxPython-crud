import wx
from wx import xrc
from controller.usercontroller import UserController
from controller.register import RegistroFrame
from controller.conection import Conection
from controller.addGames import RegistroGame
from controller.addSeries import RegistroSerie
from controller.modific import ModificFrame
from model.model import User, Serie, Videojuego
from sqlalchemy.orm.exc import MultipleResultsFound
from controller.series import Series
from controller.videogames import VideoGame
from controller.vistaSerie import VistaSerie
from controller.vistaGame import vistaGame

UPDATE_USER = "Update User"
DELETE_USER = "Delete User"

class InicioFrame(wx.Frame):

    def __init__(self):
        super(InicioFrame, self).__init__()
        self.res = xrc.XmlResource('../view/inicio.xrc')
        self.user_controller = UserController()
        self.conect = Conection()
        self.series = Series()
        self.games = VideoGame()
        self.grid_sizer = None
        self.add_user_frame = None
        self.update_users = None
        self.user_selected = None
        self.add_series = None
        self.add_games = None
        self.list_user = []
        self.list_serie = []
        self.frame = self.res.LoadFrame(None, 'InicioFrame')
        self.panel = xrc.XRCCTRL(self.frame, 'InicioPanel')
        self.listbook_menu = xrc.XRCCTRL(self.panel, 'listbook')
        self.panel_users = xrc.XRCCTRL(self.listbook_menu, 'panel2')
        self.listctrl_users = xrc.XRCCTRL(self.panel_users, 'listControl')
        self.button_add_user = xrc.XRCCTRL(self.panel_users, 'addUser')
        self.load_columns_listcrtl_user()
        self.load_data_listctrl_user()

        #Users
        self.frame.Bind(wx.EVT_BUTTON, self.create_user, self.button_add_user)
        self.frame.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_user_selected, self.listctrl_users)
        self.text_search = xrc.XRCCTRL(self.panel_users, 'textCtrlSearch')
        self.button_search = xrc.XRCCTRL(self.panel_users, 'search')
        self.frame.Bind(wx.EVT_BUTTON, self.search_user, self.button_search)
        # Exit Buttons
        self.button_exit = xrc.XRCCTRL(self.panel_users, 'logOut')
        self.frame.Bind(wx.EVT_BUTTON, self.close_frames, self.button_exit)

        #Series
        self.panel_serie = xrc.XRCCTRL(self.listbook_menu, 'panelSeries')
        self.grid_serie = xrc.XRCCTRL(self.panel_serie, 'scrolledWindowserie')
        self.grid_sizer_series()

        self.text_search_serie = xrc.XRCCTRL(self.panel_serie, 'textCtrlSerie')
        self.button_search_serie = xrc.XRCCTRL(self.panel_serie, 'searchSerie')
        self.frame.Bind(wx.EVT_BUTTON, self.search_serie, self.button_search_serie)
        self.button_exit_series = xrc.XRCCTRL(self.panel_users, 'logOut')
        self.Bind(wx.EVT_BUTTON, self.close_frames, self.button_exit_series)
        # Button Add series
        self.button_add_serie = xrc.XRCCTRL(self.panel_serie, 'addSerie')
        self.frame.Bind(wx.EVT_BUTTON, self.open_add_serie, self.button_add_serie)

        #Games
        self.panel_game = xrc.XRCCTRL(self.listbook_menu, 'panelGames')
        self.grid_game = xrc.XRCCTRL(self.panel_game, 'scrolledWindowGame')
        self.grid_sizer_games()

        self.text_search_game = xrc.XRCCTRL(self.panel_game, 'textCtrlGame')
        self.button_search_game = xrc.XRCCTRL(self.panel_game, 'searchGame')
        self.frame.Bind(wx.EVT_BUTTON, self.search_game, self.button_search_game)
        self.button_exit_games = xrc.XRCCTRL(self.panel_users, 'logOut')
        self.Bind(wx.EVT_BUTTON, self.close_frames, self.button_exit_games)
        #Button Add Games
        self.button_add_game = xrc.XRCCTRL(self.panel_game, 'addGame')
        self.frame.Bind(wx.EVT_BUTTON, self.open_add_game, self.button_add_game)

        self.frame.Show()

    # Se puede mejorar la funcion de buscar series de manera que retorne el boton de la serie mas no un mensaje solamente.
    def search_serie(self, evt):
        text_serie = str(self.text_search_serie.GetValue())
        session = self.conect.connect_database()

        try:
            serie = session.query(Serie).filter_by(titulo_serie=text_serie).all()
            if text_serie != "":
                if serie:

                    wx.MessageBox('The serie exist in this aplication.')

                else:
                    wx.MessageBox('The serie does not exist in this aplication.')

            else:
                wx.MessageBox('Fields no entered.')

            session.close()

        except MultipleResultsFound:
            session.close()
            return False

    # Se puede mejorar la funcion de buscar juegos de manera que retorne el boton del juego mas no un mensaje solamente.
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
        VistaSerie(id_serie=id_serie)


    def click_images_game(self, evt):
        id_game = evt.GetEventObject().GetName()
        vistaGame(id_game=id_game)

    def open_add_serie(self, evt):
        self.add_series = RegistroSerie(self)

    def open_add_game(self, evt):
        self.add_games = RegistroGame(self)

    def search_user(self, evt):
        text = str(self.text_search.GetValue())
        session = self.conect.connect_database()

        try:
            user = session.query(User).filter_by(first_name=text).all()
            if text != "":
                if user:
                    self.load_data_listctrl_name(text)
                    return True

                else:
                    wx.MessageBox('User does not exist in the database')
                    return self.load_data_listctrl_user()

            else:
                wx.MessageBox('Fields no entered')
                self.load_data_listctrl_user()

            session.close()

        except MultipleResultsFound:
            session.close()
            return False

    def close_frames(self, evt):
        self.frame.Destroy()

    def load_columns_listcrtl_user(self):
        self.listctrl_users.InsertColumn(0, "Id", format=wx.LIST_FORMAT_CENTER,  width=wx.LIST_AUTOSIZE)
        self.listctrl_users.InsertColumn(1, "First Name", format=wx.LIST_FORMAT_CENTER, width=wx.LIST_AUTOSIZE)
        self.listctrl_users.InsertColumn(2, "Last Name", format=wx.LIST_FORMAT_CENTER, width=wx.LIST_AUTOSIZE)
        self.listctrl_users.InsertColumn(3, "UserName", format=wx.LIST_FORMAT_CENTER, width=wx.LIST_AUTOSIZE)
        self.listctrl_users.InsertColumn(4, "Password", format=wx.LIST_FORMAT_CENTER, width=wx.LIST_AUTOSIZE)


    def load_data_listctrl_user(self):
        self.list_user = self.user_controller.get_all_users()
        self.listctrl_users.DeleteAllItems()

        for user in self.list_user:
            if len(self.list_user) > 1:
                self.listctrl_users.Append([user.id, user.first_name, user.last_name, user.username, user.password])

    def load_data_listctrl_name(self, name):
        user = self.user_controller.get_first_name(name)
        self.listctrl_users.DeleteAllItems()

        for item in user:
            self.listctrl_users.Append([item.id, item.first_name, item.last_name, item.username, item.password])

    def create_user(self, evt):
        self.add_user_frame = RegistroFrame(self)

    def list_user_selected(self, evt):
        current_item = evt.GetIndex()
        self.user_selected = self.list_user[current_item]
        menu = wx.Menu()
        id_item_menu_update = wx.NewId()
        id_item_menu_delete = wx.NewId()
        menu.Append(id_item_menu_update, UPDATE_USER)
        menu.Append(id_item_menu_delete, DELETE_USER)
        self.frame.Bind(wx.EVT_MENU, self.popup_item_selected, id=id_item_menu_update)
        self.frame.Bind(wx.EVT_MENU, self.popup_item_selected, id=id_item_menu_delete)
        self.frame.PopupMenu(menu)
        menu.Destroy()

    def popup_item_selected(self, evt):
        id_item = evt.GetId()
        menu = evt.GetEventObject()
        menu_item = menu.FindItemById(id_item)

        if menu_item.GetLabel() == UPDATE_USER:
            self.add_user_frame = ModificFrame(self, self.user_selected.id)

        elif menu_item.GetLabel() == DELETE_USER:
            msg = "Is you sure to delete the User %s %s?" % (self.user_selected.first_name, self.user_selected.last_name)
            result = wx.MessageBox(msg, "Delete User", wx.YES_NO | wx.ICON_EXCLAMATION)

            if result == wx.YES:
                self.user_controller.delete_user(self.user_selected.id)
                self.load_data_listctrl_user()

if __name__ == '__main__':
    app = wx.App()
    frame = InicioFrame()
    app.MainLoop()
