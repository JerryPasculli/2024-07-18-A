import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        o1 = self._view.dd_min_ch.value
        o2 = self._view.dd_max_ch.value
        print(o1)
        print(o2)
        if o1 is None or o2 is None or int(o1)>int(o2):
            t1 = ft.Text("HAI SCELTO UNA FINESTRA SBAGLIATA", color="red")
            self._view.txt_result1.controls.append(t1)
            self._view.update_page()
            return
        testo = self._model.creaArco(int(o1), int(o2))
        self._view.txt_result1.controls.append(ft.Text(testo))
        self._view.update_page()

    def handle_dettagli(self, e):
        pass

    def popola(self):
        lista = self._model.cromos()
        for element in lista:
            opt = ft.dropdown.Option(element[0])
            self._view.dd_min_ch.options.append(opt)
            self._view.dd_max_ch.options.append(opt)

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        t1 = self._model.percorso()
        self._view.txt_result2.controls.append(ft.Text(t1))
        self._view.update_page()
