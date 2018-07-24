import unreal_engine as ue

ue.exec("ms_Init.py")

app = QtWidgets.QApplication(sys.argv)

def ticker_loop(delta_time):
    app.processEvents()
    return True

ticker = ue.add_ticker(ticker_loop)