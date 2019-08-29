import wx
from wx import xrc
from controller.videogames import VideoGame

class RegistroGame(wx.Frame):
    def __init__(self, frame_father=None, id_game=None):
        super(RegistroGame, self).__init__()
        self.res = xrc.XmlResource('../view/games.xrc')
        self.game = VideoGame()
        self.frame = self.res.LoadFrame(None, 'RegistroGame')
        self.id_game = id_game
        self.panel = xrc.XRCCTRL(self.frame, 'panelGame')
        self.titulo_videojuego = xrc.XRCCTRL(self.panel, 'textCtrlNameGame')
        self.compania = xrc.XRCCTRL(self.panel, 'textCtrlCompanyGame')
        self.genero = xrc.XRCCTRL(self.panel, 'textCtrlGender')
        self.horas_duracion = xrc.XRCCTRL(self.panel, 'textCtrlDurationGame')
        self.estado = xrc.XRCCTRL(self.panel, 'textCtrlStateGame')
        self.imagen_url = xrc.XRCCTRL(self.panel, 'fileLocationGame')
        self.button_save = xrc.XRCCTRL(self.panel, 'wxID_OK')
        self.button_cancel = xrc.XRCCTRL(self.panel, 'wxID_CANCEL')

        self.frame.Bind(wx.EVT_BUTTON, self.close_frame, self.button_cancel)
        self.frame.Bind(wx.EVT_BUTTON, self.create_game, self.button_save)

        self.frame.Show()

        if frame_father is not None:
            self.frame_father = frame_father

        if self.id_game is not None:
            self.load_data_game()

    def close_frame(self, evt):
        self.frame.Close()

    def create_game(self, evt):
        titulo_videojuego = self.titulo_videojuego.GetValue()
        compania = self.compania.GetValue()
        genero = self.genero.GetValue()
        horas_duracion = self.horas_duracion.GetValue()
        estado = self.estado.GetValue()
        imagen_url = self.imagen_url.GetPath()

        if titulo_videojuego and compania and genero and horas_duracion and estado and imagen_url:

            if self.id_game is not None:
                data = {'titulo_videojuego': titulo_videojuego, 'compania': compania, 'genero': genero, 'horas_duracion': horas_duracion, 'estado': estado, 'imagen_url': imagen_url}
                self.game.edit_game(self.id_game, data)
                self.load_data_game()

            else:
                self.game.create_game(titulo_videojuego, compania, genero, horas_duracion, estado, imagen_url)
                wx.MessageBox('The game has been created successfully', 'Information', wx.OK | wx.ICON_INFORMATION)
                self.clear_fields()

            self.frame_father.grid_sizer_games()

        else:
            wx.MessageBox('Fields not entered', 'Error', wx.OK | wx.ICON_ERROR)
            self.frame_father.grid_sizer_games()

    def clear_fields(self):
        self.titulo_videojuego.Clear()
        self.compania.Clear()
        self.genero.Clear()
        self.horas_duracion.Clear()
        self.estado.Clear()
        #self.imagen_url.Clear()

    def load_data_game(self):
        game = self.game.get_game(self.id_game)
        self.titulo_videojuego.SetValue(game.titulo_videojuego)
        self.compania.SetValue(game.compania)
        self.genero.SetValue(game.genero)
        self.horas_duracion.SetValue(game.horas_duracion)
        self.estado.SetValue(game.estado)
        self.imagen_url.SetValue(game.imagen_url)

if __name__ == '__main__':
    app = wx.App()
    frame = RegistroGame()
    app.MainLoop()