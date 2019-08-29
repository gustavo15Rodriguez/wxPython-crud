import wx
from wx import xrc
from controller.series import Series

class VistaSerie(wx.Frame):

    def __init__(self, id_serie, *args, **kw):
        super(VistaSerie, self).__init__(*args, **kw)
        self.res = xrc.XmlResource('../view/vistas_serie.xrc')
        self.frame = self.res.LoadFrame(None, 'VistaSerie')
        self.id_serie = id_serie
        self.series = Series()
        self.panel = xrc.XRCCTRL(self.frame, 'panelDif')
        self.text_name_serie = xrc.XRCCTRL(self.panel, 'textCtrlName')
        self.text_creator = xrc.XRCCTRL(self.panel, 'textCtrlCreator')
        self.text_gender_serie = xrc.XRCCTRL(self.panel, 'textCtrlGender')
        self.text_temporates_serie = xrc.XRCCTRL(self.panel, 'textCtrlTemporates')
        self.text_estate_serie = xrc.XRCCTRL(self.panel, 'textCtrlState')
        self.text_address_serie = xrc.XRCCTRL(self.panel, 'filePickerSerie')

        #Botones de acciones
        self.buttton_rent = xrc.XRCCTRL(self.panel, 'Rent')
        self.button_eliminte = xrc.XRCCTRL(self.panel, 'Eliminate')
        self.frame.Bind(wx.EVT_BUTTON, self.eliminate_serie, self.button_eliminte)
        self.button_modific = xrc.XRCCTRL(self.panel, 'modific')
        self.frame.Bind(wx.EVT_BUTTON, self.update_serie, self.button_modific)

        self.get_datos_serie()

        self.frame.Show()

    def eliminate_serie(self, evt):
        msg = "Is you sure to delete the Serie?"
        result = wx.MessageBox(msg, "Delete Serie", wx.YES_NO | wx.ICON_EXCLAMATION)

        if result == wx.YES:
            self.series.delete_serie(id_serie=self.id_serie)
            wx.MessageBox("The serie has been eliminated successfully!")
            self.frame.Close()

    def get_datos_serie(self):
        self.result = self.series.get_serie(id_serie=self.id_serie)
        self.text_name_serie.SetLabel(self.result.titulo_serie)
        self.text_creator.SetLabel(self.result.creador)
        self.text_gender_serie.SetLabel(self.result.genero)
        self.text_temporates_serie.SetLabel(str(self.result.no_temporadas))
        self.text_estate_serie.SetLabel(self.result.estado)
        self.text_address_serie.SetPath(self.result.imagen_url)

    def update_serie(self, evt):
        titulo_serie = self.text_name_serie.GetValue()
        creador = self.text_creator.GetValue()
        genero = self.text_gender_serie.GetValue()
        no_temporadas = self.text_temporates_serie.GetValue()
        estado = self.text_estate_serie.GetValue()
        imagen_url = self.text_address_serie.GetPath()

        if titulo_serie and creador and genero and no_temporadas and estado and imagen_url:

            if self.id_serie is not None:
                data = {'titulo_serie': titulo_serie, 'creador': creador, 'genero': genero, 'no_temporadas': no_temporadas, 'estado': estado, 'imagen_url': imagen_url}
                self.series.edit_series(self.id_serie, data)
                wx.MessageBox('The serie has been update successfully', 'Information', wx.OK | wx.ICON_INFORMATION)

        else:
            wx.MessageBox('Fields not entered', 'Error', wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    frame = VistaSerie()
    app.MainLoop()