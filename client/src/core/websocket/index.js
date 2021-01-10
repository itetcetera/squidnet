import React, { useState } from 'react'
import SocketIOClient from 'socket.io-client'

function Websocker(){

    const [image, setImage] = useState('')

    var socket = SocketIOClient('https://squidnet.herokuapp.com')

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