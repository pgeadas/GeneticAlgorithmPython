# -*- coding: utf-8 -*-
from locale import atof, atoi
import wx
from matplotlib import pyplot as plt

from SGA_BC import sga


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400, 450))
        self.CreateStatusBar()

        # Modern font initialization
        self.font1 = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # UI setup
        self.create_controls()
        self.create_menu()
        self.layout_ui()
        self.Show(True)

    def create_controls(self):
        quoteList = [
            'Number of Generations:', 'Population Size:', 'Number of Points:', 'Target:',
            'Size of Tournament/Roullete:', 'Crossover Probability (0 to 1):',
            'Number of Crossover Points:', 'Mutation Probability: (0 to 1)',
            'Elite Percentage (0 to 1):', 'Selection Method (1-Tournament, 2-Roullete):',
            '1-Equal Partitions, 2-Random Partitions', '1-Normal Mutation, 2-Gaussian Mutation\n'
        ]
        defaultValues = ['4', '10', '5', '[150,75,200,25]', '3', '0.5', '1', '0.1', '0.2', '1', '2', '1']

        self.buttons = [wx.Button(self, -1, " Start Work!")]
        self.tFields = [wx.TextCtrl(self, value=val) for val in defaultValues]
        self.quotes = [wx.StaticText(self, label=text) for text in quoteList]

        # Modern color handling
        for quote in self.quotes:
            quote.SetForegroundColour(wx.WHITE)
            quote.SetFont(self.font1)

        self.logger = wx.TextCtrl(self, size=(300, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)

    def create_menu(self):
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, "Open File")
        file_menu.Append(wx.ID_ABOUT, "About")
        file_menu.Append(wx.ID_EXIT, "Exit")
        menubar.Append(file_menu, "&File")
        self.SetMenuBar(menubar)

        # Modern event binding
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_BUTTON, self.OnClickStart, self.buttons[0])

    def layout_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(5, 5)

        # Add controls to grid
        for idx, (quote, field) in enumerate(zip(self.quotes, self.tFields)):
            grid.Add(quote, (idx, 0), flag=wx.ALIGN_CENTER_VERTICAL)
            grid.Add(field, (idx, 1), flag=wx.EXPAND)

        # Assemble main layout
        main_sizer.Add(grid, 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self.logger, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.buttons[0], 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(main_sizer)
        self.Layout()

    # Event handlers
    def OnAbout(self, event):
        with wx.MessageDialog(self,
                              "Developed by:\n\nPedro Geadas\n2006131902\npmrg@student.dei.uc.pt",
                              "About", wx.OK) as dlg:
            dlg.ShowModal()

    def OnExit(self, event):
        self.Close()

    def OnOpen(self, event):
        with wx.FileDialog(self, "Choose a file", style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                with open(dlg.GetPath(), 'r') as f:
                    self.logger.SetValue(f.read())

    def OnClickStart(self, event):
        # Parameter validation logic
        try:
            params = self.validate_parameters()
            if not params:
                return

            # Run GA
            results = sga(*params)

            # Process data: x_cor and y_cor
            x_cor = []
            y_cor = []
            for i in range(len(results[1])):
                if i % 2 == 0:
                    x_cor.append(results[1][i])
                else:
                    y_cor.append(results[1][i])

            plt.ylabel('Y')
            plt.xlabel('X')
            plt.title('Brachistochrone Curve')
            plt.plot(x_cor, y_cor, label="Best")
            plt.legend(loc='upper right')
            plt.show()

        except Exception as e:
            self.logger.AppendText(f"\nError: {str(e)}\n")

    def validate_parameters(self):
        try:
            params = [
                int(self.tFields[0].GetValue()),
                int(self.tFields[1].GetValue()),
                int(self.tFields[2].GetValue()),
                self.parse_target(self.tFields[3].GetValue()),
                int(self.tFields[4].GetValue()),
                float(self.tFields[5].GetValue()),
                int(self.tFields[6].GetValue()),
                float(self.tFields[7].GetValue()),
                float(self.tFields[8].GetValue()),
                int(self.tFields[9].GetValue()),
                int(self.tFields[10].GetValue()),
                int(self.tFields[11].GetValue()),
                30  # times parameter
            ]

            if params[1] % 2 != 0:
                raise ValueError("Population size must be even")
            if params[2] <= params[6]:
                raise ValueError("Number of points must be greater than crossover points")

            return params

        except ValueError as e:
            self.logger.AppendText(f"\nValidation Error: {str(e)}\n")
            return None

    def parse_target(self, target_str):
        try:
            if not (target_str.startswith('[') and target_str.endswith(']')):
                raise ValueError
            values = [float(x.strip()) for x in target_str[1:-1].split(',')]
            if len(values) != 4:
                raise ValueError
            if values[3] >= values[1]:
                raise ValueError("Target yf must be < yi")
            if values[2] <= values[0]:
                raise ValueError("Target xf must be > xi")
            return values
        except:
            raise ValueError("Invalid target format. Use [xi,yi,xf,yf]")


if __name__ == "__main__":
    app = wx.App()
    MainWindow(None, "Inteligência Artificial - TP2")
    app.MainLoop()
