import wx
from wx import xrc
from controller.series import Series
from controller.conection import Conection
from model.model import Rentas

class VistaUserSerie(wx.Frame):

    def __init__(self, id_serie, id_user, *args, **kw):
        super(VistaUserSerie, self).__init__(*args, **kw)
        self.res = xrc.XmlResource('../view/vistas_serie_user.xrc')
        self.frame = self.res.LoadFrame(None, 'VistaUserSerie')
        self.panel = xrc.XRCCTRL(self.frame, 'panelOptions')

        self.id_serie = id_serie
        self.id_user = id_user
        self.rents = Rentas()
        self.series = Series()
        self.conect = Conection()

        self.text_name_serie = xrc.XRCCTRL(self.panel, 'staticTextName')
        self.text_creator = xrc.XRCCTRL(self.panel, 'staticTextCreator')
        self.text_gender_serie = xrc.XRCCTRL(self.panel, 'staticTextGenero')
        self.text_temporates_serie = xrc.XRCCTRL(self.panel, 'staticTextTemporates')
        self.text_estate_serie = xrc.XRCCTRL(self.panel, 'staticTextEstado')

        self.button_rent = xrc.XRCCTRL(self.panel, 'rent')
        self.frame.Bind(wx.EVT_BUTTON, self.rent_selected, self.button_rent)
        self.button_exit = xrc.XRCCTRL(self.panel, 'cancel')
        self.frame.Bind(wx.EVT_BUTTON, self.close_frame, self.button_exit)

        self.get_datos_serie()

        self.frame.Show()

    def close_frame(self, evt):
        self.frame.Close()

    # Corregir los errores a la hora de eliminar las series rentadas.
    def rent_selected(self, evt):
        result = wx.MessageBox('Do you really want to rent this serie?', 'Information', wx.YES_NO | wx.ICON_EXCLAMATION)
        self.result = self.series.get_serie(id_serie=self.id_serie)

        if result == wx.YES:
            session = self.conect.connect_database()
            new_state = "Prestado"

            if self.result.estado == "Entregado":
                self.result.estado = new_state
                rent = Rentas(id_usuario=self.id_user, id_renta=self.id_serie, estado_renta=self.result.estado)
                session.add(rent)
                session.commit()
                session.close()
                wx.MessageBox('The rent has been rented correctly', 'Information', wx.OK | wx.ICON_INFORMATION)
                self.frame.Close()

                if self.id_serie is not None:
                    data = {'estado': self.result.estado}
                    self.series.edit_state(self.id_serie, data)

                else:
                    return None

            elif self.result.estado == "Prestado":
                rent = session.query(Rentas).filter_by(id_usuario=self.id_user).one_or_none()

                if rent is not None:
                    self.rents.id_usuario = rent.id_usuario

                else:
                    self.rents.id_usuario = rent

                if self.id_user == self.rents.id_usuario:
                    result = wx.MessageBox('You have already rented this series. Do you want to return it now?', 'Information', wx.YES_NO | wx.ICON_EXCLAMATION)

                    if result == wx.YES:
                        session = self.conect.connect_database()
                        rent_deliver = session.query(Rentas).filter_by(id_renta=self.id_serie).one()
                        session.delete(rent_deliver)

                        self.result.estado = 'Entregado'
                        data = {'estado': self.result.estado}
                        self.series.edit_state(self.id_serie, data)
                        wx.MessageBox('The rent has been delivered correctly', 'Information', wx.OK | wx.ICON_INFORMATION)
                        self.frame.Close()
                        session.close()
                else:
                    wx.MessageBox('You have not been the person who has rented this serie, therefore you cannot return or lend it until it is returned.', 'Information', wx.OK | wx.ICON_INFORMATION)

            session.close()

    def get_datos_serie(self):
        self.result = self.series.get_serie(id_serie=self.id_serie)
        self.text_name_serie.SetLabel(self.result.titulo_serie)
        self.text_creator.SetLabel(self.result.creador)
        self.text_gender_serie.SetLabel(self.result.genero)
        self.text_temporates_serie.SetLabel(str(self.result.no_temporadas))
        self.text_estate_serie.SetLabel(self.result.estado)

if __name__== '__main__':
    app = wx.App()
    frame = VistaUserSerie()
    app.MainLoop()
