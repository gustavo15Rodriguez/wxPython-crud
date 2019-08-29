import wx
from wx import xrc
from controller.videogames import VideoGame

class vistaGame(wx.Frame):

    def __init__(self, id_game, *args, **kw):

        super(vistaGame, self).__init__(*args, **kw)
        self.res = xrc.XmlResource('../view/vistas_game.xrc')
        self.frame = self.res.LoadFrame(None, 'vistaGame')
        self.panel = xrc.XRCCTRL(self.frame, 'panelgame')
        self.game = VideoGame()
        self.id_game = id_game
        self.text_name_game = xrc.XRCCTRL(self.panel, 'textCtrlName')
        self.text_company = xrc.XRCCTRL(self.panel, 'textCtrlCompany')
        self.text_gender_game = xrc.XRCCTRL(self.panel, 'textCtrlGender')
        self.text_duration = xrc.XRCCTRL(self.panel, 'textCtrlDuration')
        self.text_estate_game = xrc.XRCCTRL(self.panel, 'textCtrlState')
        self.text_address_game = xrc.XRCCTRL(self.panel, 'filePickerGame')

        #Botones de acciones
        self.buttton_rent = xrc.XRCCTRL(self.panel, 'Rent')
        self.button_eliminte = xrc.XRCCTRL(self.panel, 'Eliminate')
        self.frame.Bind(wx.EVT_BUTTON, self.eliminate_game, self.button_eliminte)
        self.button_modific = xrc.XRCCTRL(self.panel, 'modific')
        self.frame.Bind(wx.EVT_BUTTON, self.update_game, self.button_modific)
        self.get_datos_game()

        self.frame.Show()

    def eliminate_game(self, evt):
        msg = "Is you sure to delete the Videogame?"
        result = wx.MessageBox(msg, "Delete Videogame", wx.YES_NO | wx.ICON_EXCLAMATION)

        if result == wx.YES:
            self.game.delete_game(id_game=self.id_game)
            wx.MessageBox("The game has been eliminate successfully!")
            self.frame.Close()


    def get_datos_game(self):
        self.result = self.game.get_game(id_game=self.id_game)
        self.text_name_game.SetLabel(self.result.titulo_videojuego)
        self.text_company.SetLabel(self.result.compania)
        self.text_gender_game.SetLabel(self.result.genero)
        self.text_duration.SetLabel(str(self.result.horas_duracion))
        self.text_estate_game.SetLabel(self.result.estado)
        self.text_address_game.SetPath(self.result.imagen_url)

    def update_game(self, evt):
        name_game = self.text_name_game.GetValue()
        company = self.text_company.GetValue()
        gender_game = self.text_gender_game.GetValue()
        duration = self.text_duration.GetValue()
        estate_game = self.text_estate_game.GetValue()
        address_game = self.text_address_game.GetPath()

        if name_game and company and gender_game and duration and estate_game and address_game:

            if self.id_game is not None:
                data = {'titulo_videojuego': name_game, 'compania': company, 'genero': gender_game, 'horas_duracion': duration, 'estado': estate_game, 'imagen_url': address_game}
                self.game.edit_game(self.id_game, data)
                wx.MessageBox('The game has been update successfully', 'Information', wx.OK | wx.ICON_INFORMATION)

        else:
            wx.MessageBox('Fields not entered', 'Error', wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    frame = vistaGame()
    app.MainLoop()