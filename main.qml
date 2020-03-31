import QtQuick 2.0
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Rectangle {
    SystemPalette {
        id: myPalette
        colorGroup: SystemPalette.Active
    }

    id: appWindow
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

                font.family: "Ubuntu"
                font.pixelSize: 48

                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 48
            }

            Text {
                text: qsTr("A placement visualizer")

                font.family: "Ubuntu"
                font.pixelSize: 16

                Layout.alignment: Qt.AlignHCenter
            }

            Item {
                Layout.fillHeight: true
            }

            Text {
                text: qsTr("Created by Kevin Abraham<br>and Himanshu Yadav")

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

                font.family: "Ubuntu"
                font.pixelSize: 16

                Layout.alignment: Qt.AlignHCenter
            }

            RowLayout {
                spacing: 0

                Rectangle {
                    color: "LightGray"

                    width: 1
                    Layout.fillHeight: true
                }

                ListView {
                    id: listView
                    clip: true

                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    model: ListModel {
                        ListElement {
                            name: "biomedP"
                            path: "benchmarks/biomedP.hgr"
                            placed: false
                        }
                        ListElement {
                            name: "industry2"
                            path: "benchmarks/industry2.hgr"
                            placed: false
                        }
                        ListElement {
                            name: "industry3"
                            path: "benchmarks/industry3.hgr"
                            placed: true
                        }
                        ListElement {
                            name: "p2"
                            path: "benchmarks/p2.hgr"
                            placed: false
                        }
                        ListElement {
                            name: "structP"
                            path: "benchmarks/structP.hgr"
                            placed: true
                        }
                    }

                    delegate: Item {
                        height: benchmarkButton.height - 1

                        anchors.left: parent.left
                        anchors.right: parent.right

                        Button {
                            id: benchmarkButton
                            height: 49

                            anchors.left: parent.left
                            anchors.right: parent.right

                            background: Rectangle {
                                color: benchmarkButton.down ? "LightGray" : "transparent"
                                border.color: "LightGray"
                                border.width: 1
                            }

                            Rectangle {
                                id: benchmarkStatus
                                color: placed ? "green" : "red"
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
                                text: name

                                anchors {
                                    top: parent.top
                                    topMargin: 8
                                    left: parent.left
                                    leftMargin: 16
                                }
                            }

                            Text {
                                id: benchmarkPath
                                text: path
                                color: "gray"

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
