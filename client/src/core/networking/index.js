import React from "react"
import {
    Header,
    Segment
} from 'semantic-ui-react'

import SquidHeader from "../../common/components/SquidHeader"


function NetworkPage() {

    return (
        <div>
            <SquidHeader />

            <Segment style={{ marginTop: '90px' }}>
                <Header>How many tickles does it take to get a squid to laugh? Ten Tickles!</Header>
            </Segment>
        </div>
    )
}

export default NetworkPage