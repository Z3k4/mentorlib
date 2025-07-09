class ChatSocket {
    templateChatHTML = ""
    parent = document.querySelector("body")
    init(roomName) {
        this.roomName = roomName
        this.socket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        )

    }

    setParent(parent) {
        this.parent = parent
    }

    setTemplateHandle(template) {
        this.templateChatHTML = this.templateChatHTML
    }
}