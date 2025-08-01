class Socket {
    templateChatHTML = ""
    parent = document.querySelector("body")
    init(roomName, link) {
        this.roomName = roomName
        this.socket = new WebSocket(
            'ws://'
            + window.location.host
            + link
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

export {Socket}