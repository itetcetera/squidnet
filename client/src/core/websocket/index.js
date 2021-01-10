import React, { useState } from 'react'
import SocketIOClient from 'socket.io-client'

function Websocker(){

    const [image, setImage] = useState('')

    var socket = SocketIOClient('http://127.0.0.1:5000')

    socket.on('connect', () => {
        console.log('HYPR')
    })

    socket.on('receive_image', response => { 
        console.log(response) 
        setImage(response)
    })

    return (
        <div>
            <img src={"data:image/png;base64," + image} />
        </div>
    )
}

export default Websocker