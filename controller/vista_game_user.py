import wx
from wx import xrc
from controller.videogames import VideoGame
from controller.conection import Conection
from model.model import Rentas

class VistaGameUser(wx.Frame):

    def __init__(self, id_game, id_user, *args, **kw):
        super(VistaGameUser, self).__init__(*args, **kw)
        self.res = xrc.XmlResource('../view/vistas_game_user.xrc')
        self.frame = self.res.LoadFrame(None, 'VistaGameUser')
        self.panel = xrc.XRCCTRL(self.frame, 'panelData')

        self.id_game = id_game
        self.id_user = id_user
        self.game = VideoGame()
        self.conect = Conection()
        self.rents = Rentas()

        self.text_name_game = xrc.XRCCTRL(self.panel, 'staticTextName')
        self.text_company = xrc.XRCCTRL(self.panel, 'staticTextCompany')
        self.text_gender_game = xrc.XRCCTRL(self.panel, 'staticTextGenero')
        self.text_duration = xrc.XRCCTRL(self.panel, 'staticTextDuration')
        self.text_estate_game = xrc.XRCCTRL(self.panel, 'staticTextEstado')

        self.button_rent = xrc.XRCCTRL(self.panel, 'buttonRent')
        self.frame.Bind(wx.EVT_BUTTON, self.rent_selected, self.button_rent)

        self.button_exit = xrc.XRCCTRL(self.panel, 'buttonCancel')
        self.frame.Bind(wx.EVT_BUTTON, self.close_frame, self.button_exit)

        self.get_datos_game()

        self.frame.Show()

    # Corregir errores a la hora de eliminar los videojuegos rentados
    def rent_selected(self, evt):
        result = wx.MessageBox('Do you really want to rent this videogame?', 'Information', wx.YES_NO | wx.ICON_EXCLAMATION)
        self.result = self.game.get_game(id_game=self.id_game)

        if result == wx.YES:
            session = self.conect.connect_database()
            new_state = "Prestado"

            if self.result.estado == "Entregado":
                self.result.estado = new_state
                rent = Rentas(id_usuario=self.id_game, id_renta=self.id_game, estado_renta=self.result.estado)
                session.add(rent)
                session.commit()
                session.close()
                wx.MessageBox('The rent has been rented correctly', 'Information', wx.OK | wx.ICON_INFORMATION)
                self.frame.Close()

                if self.id_game is not None:
                    data = {'estado': self.result.estado}
                    self.game.edit_state(self.id_game, data)

                else:
                    return None

            elif self.result.estado == "Prestado":
                rent = session.query(Rentas).filter_by(id_usuario=self.id_user).one_or_none()

                if rent is not None:
                    self.rents.id_usuario = rent.id_usuario

                else:
                    self.rents.id_usuario = rent

                if self.id_user == self.rents.id_usuario:
                    result = wx.MessageBox('You have already rented this videogame. Do you want to return it now?', 'Information', wx.YES_NO | wx.ICON_EXCLAMATION)

                    if result == wx.YES:
                        session = self.conect.connect_database()
                        rent_deliver = session.query(Rentas).filter_by(id_renta=self.id_game).one()
                        session.delete(rent_deliver)

                        self.result.estado = 'Entregado'
                        data = {'estado': self.result.estado}
                        self.game.edit_state(self.id_game, data)
                        wx.MessageBox('The rent has been delivered correctly', 'Information', wx.OK | wx.ICON_INFORMATION)
                        self.frame.Close()
                        session.close()
                else:
                    wx.MessageBox('You have not been the person who has rented this video game, therefore you cannot return or lend it until it is returned.', 'Information', wx.OK | wx.ICON_INFORMATION)

            session.close()

    def close_frame(self, evt):
        self.frame.Close()

    def get_datos_game(self):
        self.result = self.game.get_game(id_game=self.id_game)
        self.text_name_game.SetLabel(self.result.titulo_videojuego)
        self.text_company.SetLabel(self.result.compania)
        self.text_gender_game.SetLabel(self.result.genero)
        self.text_duration.SetLabel(str(self.result.horas_duracion))
        self.text_estate_game.SetLabel(self.result.estado)

if __name__== '__main__':
    app = wx.App()
    frame = VistaGameUser()
    app.MainLoop()
