import QtQuick 2.0

QtObject {
    property var startScreen: StartScreen {
        visible: true
    }
    property var loadingDialog: LoadingScreen {
        visible: false
    }
}
