import wx
from wx import xrc
from controller.series import Series
from controller.conection import Conection

class RegistroSerie(wx.Frame):

    def __init__(self, frame_father=None, id_serie=None):
        super(RegistroSerie, self).__init__()
        self.res = xrc.XmlResource('../view/series.xrc')
        self.series = Series()
        self.conection = Conection()
        self.id_serie = id_serie
        self.frame = self.res.LoadFrame(None, 'RegistroSerie')
        self.panel = xrc.XRCCTRL(self.frame, 'm_panel6')
        self.titulo_serie = xrc.XRCCTRL(self.panel, 'textCtrlName')
        self.creador = xrc.XRCCTRL(self.panel, 'textCtrlCreator')
        self.genero = xrc.XRCCTRL(self.panel, 'textCtrlGender')
        self.no_temporadas = xrc.XRCCTRL(self.panel, 'textCtrlTemporates')
        self.estado = xrc.XRCCTRL(self.panel, 'textCtrlSate')
        self.imagen_url = xrc.XRCCTRL(self.panel, 'fileLocationSerie')
        self.button_save = xrc.XRCCTRL(self.panel, 'wxID_OK')
        self.button_cancel = xrc.XRCCTRL(self.panel, 'wxID_CANCEL')
        self.frame.Bind(wx.EVT_BUTTON, self.close_frame, self.button_cancel)

        self.frame.Bind(wx.EVT_BUTTON, self.close_frame, self.button_cancel)
        self.frame.Bind(wx.EVT_BUTTON, self.create_serie, self.button_save)

        self.frame.Show()

        if frame_father is not None:
            self.frame_father = frame_father

        if self.id_serie is not None:
            self.load_data_serie()

    def close_frame(self, evt):
        self.frame.Close()

    def create_serie(self, evt):
        titulo_serie = self.titulo_serie.GetValue()
        creador = self.creador.GetValue()
        genero = self.genero.GetValue()
        no_temporadas = self.no_temporadas.GetValue()
        estado = self.estado.GetValue()
        imagen_url = self.imagen_url.GetPath()

        if titulo_serie and creador and genero and no_temporadas and estado and imagen_url:

            if self.id_serie is not None:
                data = {'titulo_serie': titulo_serie, 'creador': creador, 'genero': genero, 'no_temporadas': no_temporadas, 'estado': estado, 'imagen_url': imagen_url}
                self.series.edit_series(self.id_serie, data)
                self.load_data_serie()

            else:
                self.series.create_serie(titulo_serie, creador, genero, no_temporadas, estado, imagen_url)
                wx.MessageBox('The serie has been created successfully', 'Information', wx.OK | wx.ICON_INFORMATION)
                self.clear_fields()

            self.frame_father.grid_sizer_series()

        else:
            wx.MessageBox('Fields not entered', 'Error', wx.OK | wx.ICON_ERROR)
        self.frame_father.grid_sizer_series()


    def clear_fields(self):
        self.titulo_serie.Clear()
        self.creador.Clear()
        self.genero.Clear()
        self.no_temporadas.Clear()
        self.estado.Clear()
        #self.imagen_url.Clear()

    def load_data_serie(self):
        serie = self.series.get_serie(self.id_serie)
        self.titulo_serie.SetValue(serie.titulo_serie)
        self.creador.SetValue(serie.creador)
        self.genero.SetValue(serie.genero)
        self.no_temporadas.SetValue(serie.no_temporadas)
        self.estado.SetValue(serie.estado)
        self.imagen_url.SetValue(serie.imagen_url)


if __name__ == '__main__':
    app = wx.App()
    frame = RegistroSerie()
    app.MainLoop()