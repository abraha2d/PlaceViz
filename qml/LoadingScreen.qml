import QtQuick 2.0
import QtQuick.Controls 2.14
import QtQuick.Window 2.14

Window {
    SystemPalette {
        id: myPalette
        colorGroup: SystemPalette.Active
    }

    color: myPalette.window
    flags: Qt.Tool | Qt.FramelessWindowHint

    width: loadingIndicator.width
    height: loadingIndicator.height

    BusyIndicator {
        id: loadingIndicator
    }
}
