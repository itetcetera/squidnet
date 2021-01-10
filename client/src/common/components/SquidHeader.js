import React from "react"
import {
    Header,
    Menu,
    Image,
} from 'semantic-ui-react'

import Logo from '../img/squidlogo_see_through.png'

function SquidHeader() {

    return (
        <Menu
            fixed='top'
            pointing
            size='large'
            style={{ backgroundColor: '#00A3FF' }}
        >
            <Image src={Logo} size='tiny' style={{ marginTop: '4px' }} />
            <Header as='h1' inverted>Squidnet.tech</Header>
        </Menu>
    )
}

export default SquidHeader