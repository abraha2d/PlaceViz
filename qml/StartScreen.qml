import QtQuick 2.0
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

ApplicationWindow {
    SystemPalette {
        id: myPalette
        colorGroup: SystemPalette.Active
    }

    width: 640
    height: 360
    color: myPalette.window

    RowLayout {
        anchors.fill: parent

        ColumnLayout {
            Layout.minimumWidth: 250
            Layout.preferredWidth: 300

            Text {
                text: qsTr("PlaceViz")
                color: myPalette.text

                font.family: "Ubuntu"
                font.pixelSize: 48

                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 48
            }

            Text {
                text: qsTr("A placement visualizer")
                color: myPalette.text

                font.family: "Ubuntu"
                font.pixelSize: 16

                Layout.alignment: Qt.AlignHCenter
            }

            Item {
                Layout.fillHeight: true
            }

            Text {
                text: qsTr("Created by Kevin Abraham<br>and Himanshu Yadav")
                color: myPalette.text

                font.family: "Ubuntu"
                font.pixelSize: 16
                horizontalAlignment: Text.AlignHCenter

                Layout.alignment: Qt.AlignHCenter
                Layout.bottomMargin: 48
            }
        }

        ColumnLayout {
            Layout.minimumWidth: 250
            Layout.fillWidth: true

            Text {
                text: qsTr("Benchmarks")
                color: myPalette.text

                font.family: "Ubuntu"
                font.pixelSize: 16

                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 8
            }

            RowLayout {
                spacing: 0

                Rectangle {
                    color: myPalette.light

                    width: 1
                    Layout.fillHeight: true
                }

                ListView {
                    id: listView
                    clip: true

                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    model: benchmarkList

                    delegate: Item {
                        height: benchmarkButton.height - 1

                        anchors.left: parent.left
                        anchors.right: parent.right

                        Button {
                            id: benchmarkButton
                            height: 49
                            onClicked: controller.benchmarkClicked(model.benchmark)

                            anchors.left: parent.left
                            anchors.right: parent.right

                            background: Rectangle {
                                color: benchmarkButton.down ? myPalette.light : benchmarkButton.hovered ? myPalette.mid : "transparent"
                                border.color: myPalette.light
                                border.width: 1
                            }

                            Rectangle {
                                id: benchmarkStatus
                                color: model.benchmark.isOther ? "transparent" : model.benchmark.isPlaced ? "green" : "red"
                                width: 4

                                anchors {
                                    top: parent.top
                                    bottom: parent.bottom
                                    left: parent.left
                                    margins: 2
                                }
                            }

                            Text {
                                id: benchmarkName
                                text: model.benchmark.name
                                color: myPalette.text

                                anchors {
                                    top: parent.top
                                    topMargin: 8
                                    left: parent.left
                                    leftMargin: 16
                                }
                            }

                            Text {
                                id: benchmarkPath
                                text: model.benchmark.path
                                color: myPalette.dark

                                anchors {
                                    top: benchmarkName.bottom
                                    topMargin: 4
                                    left: parent.left
                                    leftMargin: 16
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
