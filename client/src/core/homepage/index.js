import React from "react"
import {
    Header,
    Segment,
    Grid,
    Divider,
    Icon,
    Input,
    Container,
    Button
} from 'semantic-ui-react'

import SquidHeader from "../../common/components/SquidHeader"


function HomePage() {

    return (
        <div>
            <SquidHeader />

            <Segment style={{ marginTop: '90px' }}>
                <Grid columns={2} stackable textAlign='center' style={{ height: '500px' }}>
                    <Divider vertical style={{ height: '230px' }}>Or</Divider>

                    <Grid.Row verticalAlign='middle'>
                        <Grid.Column>
                            <Header icon as='h2'>
                                <Icon name='search' />
                                Join Room
                            </Header>
                            <br />
                            <Input placeholder='Display Name...' />
                            <br />
                            <Input style={{ marginTop: '5px' }} placeholder='Room Code...' />
                            <br />
                            <Button style={{ marginTop: '5px' }} color='blue' >JOIN</Button>
                        </Grid.Column>
                        <Grid.Column>
                            <Header icon as='h2'>
                                <Icon name='tint' />
                                Create Room
                            </Header>
                            <br />
                            <Button style={{ marginTop: '20px' }} color='blue' >CREATE</Button>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Segment>
            <Container style={{ backgroundColor: '#00A3FF' }}>

            </Container>
        </div>
    )
}

export default HomePage