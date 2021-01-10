import React, { useEffect, useState } from "react"
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

var updateWindowSize;

function HomePage() {

    const [windowSize, setWindowSize] = useState(window.innerWidth)
    const [displayName, setDisplayName] = useState('')
    const [roomCode, setRoomCode] = useState('')

    updateWindowSize = () => setWindowSize(window.innerWidth)

    useEffect(() => {
        window.addEventListener('resize', updateWindowSize)

        return () => {
            window.removeEventListener('resize', updateWindowSize)
        }
    })

    var onDisplayNameChange = (newDisplay) => {
        setDisplayName(newDisplay)
    }
    var onRoomCodeChange = (newCode) => {
        setRoomCode(newCode)
    }

    return (
        <div>
            <SquidHeader />

            <Segment style={{ marginTop: '90px' }}>

                {windowSize >= 770 &&
                    (<Grid columns={2} stackable textAlign='center' style={{ height: '500px' }}>
                        <Divider vertical style={{ height: '230px' }}>Or</Divider>

                        <Grid.Row verticalAlign='middle'>
                            <Grid.Column>
                                <Header icon as='h2'>
                                    <Icon name='search' />
                                Join Room
                            </Header>
                                <br />
                                <Input
                                    style={{ width: '200px' }}
                                    placeholder='Display Name...'
                                    value={displayName}
                                    onChange={(e, v) => onDisplayNameChange(v.value)}
                                />
                                <br />
                                <Input
                                    style={{ marginTop: '5px', width: '200px' }}
                                    placeholder='Room Code...'
                                    value={roomCode}
                                    onChange={(e, v) => onRoomCodeChange(v.value)}
                                />
                                <br />
                                <Button style={{ marginTop: '5px', width: '150px' }} color='blue' >JOIN</Button>
                            </Grid.Column>
                            <Grid.Column>
                                <Header icon as='h2'>
                                    <Icon name='tint' />
                                Create Room
                            </Header>
                                <br />
                                <Input
                                    style={{ width: '200px' }}
                                    placeholder='Display Name...'
                                    value={displayName}
                                    onChange={(e, v) => onDisplayNameChange(v.value)}
                                />
                                <br />
                                <Button style={{ marginTop: '10px', width: '150px' }} color='blue' >CREATE</Button>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>)}

                {windowSize < 770 &&
                    (<div style={{ margin: '30px 0px', display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column' }}>
                        <Header icon as='h2'>
                            <Icon name='search' />
                                Join Room
                            </Header>
                        <br />
                        <Input
                            style={{ width: '200px' }}
                            placeholder='Display Name...'
                            value={displayName}
                            onChange={(e, v) => onDisplayNameChange(v.value)}
                        />
                        <br />
                        <Input
                            style={{ width: '200px' }}
                            placeholder='Room Code...'
                            value={roomCode}
                            onChange={(e, v) => onRoomCodeChange(v.value)}
                        />
                        <br />
                        <Button style={{ width: '150px' }} color='blue' >JOIN</Button>

                        <Divider style={{ marginTop: '50px', width: '90%' }} />

                        <Header icon as='h2'>
                            <Icon name='tint' />
                                Create Room
                            </Header>
                        <br />
                        <Input
                            style={{ width: '200px' }}
                            placeholder='Display Name...'
                            value={displayName}
                            onChange={(e, v) => onDisplayNameChange(v.value)}
                        />
                        <br />
                        <Button style={{ width: '150px' }} color='blue' >CREATE</Button>
                    </div>)}
            </Segment>


            <Segment raised style={{ backgroundColor: '#00A3FF', width: '100%' }}>
                <div>
                    <Header as='h1' style={{ textAlign: 'center', fontSize: '75px', color: '#FFFFFF' }} >Our Coleo-Idea</Header>
                    <Header as='h4' style={{ textAlign: 'center', color: '#FFFFFF' }} >Squid are members of the class Cephalopoda, subclass Coleoidea.</Header>
                </div>
            </Segment>
            <Container fluid style={{ width: '75%', fontSize: '20px', margin: '75px 0px' }}>
                <Header textAlign='left'>What is Squidnet?</Header>
                <p>
                    Squidnet is a low data video streaming application developed in 24 hours by four 2nd-year university students for nwHacks 2021. 
                    Since the Earth is currently facing a pandemic all of us have had the privilege of experience online classes.
                    With online classes come with a slew of online issues such as disconnections and laggy internets.
                    All 4 of us have been lucky enough to live in homes and areas that have high speed internet connections but we realize that not everyone is privy to these comforts.
                    In comes in our application Squidnet to help rectify this issue!
                </p>
                <p>
                    Squidnet takes in video from your camera, finds all the edges in the frame, strips everything away from the frame except for the edges and streams the filtered frames to others.
                    Video streaming takes up a lot of data since you are sending frames that contain potentially 640x360 pixels that each have RGB values around 60 frames a second!
                    While compression algorithms are successful in reducing the amount of data that is being downloaded we realized that most of the data is unnecessary.
                    We hope to strip the stream of all unnecessary data such as potentially color and light.
                    By reducing the frames to purely binary images of edges, the presenter can relay the visual information they desire without too much overhead.
                </p>
            </Container>
            <Container fluid style={{ width: '75%', fontSize: '20px', margin: '75px 0px' }}>
                <Header textAlign='left'>How is Squidnet?</Header>
                <p>
                    Squidnet utilizes many different types of technologies to achieve its service.
                </p>
                <p>
                    REACT.JS - The front-end of our web app (including this page) was built with React.js. Packages such as semantic-ui-react helped make the front page look clean and responsive.
                </p>
                <p>
                    FLASK - The entire web app is powered by a Flask server. 
                    The server handles our websocket functionality for the chat as well as our video streaming and video filtering.
                    Packages such as OpenCV and SocketIO were used
                </p>
                <p>
                    Heroku - We are using Heroku to host our Flask server on.
                </p>
                <p>
                    Domain.com - We also have Domain.com to thank for giving us our domain
                </p>
            </Container>




            <Segment raised style={{ backgroundColor: '#00A3FF', width: '100%' }}>
                <div>
                    <Header as='h1' style={{ textAlign: 'center', fontSize: '75px', color: '#FFFFFF' }} >Th-ink-ers Behind Everything</Header>
                </div>
            </Segment>
            <Container fluid style={{ width: '75%', fontSize: '20px' }}>
                <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
            </Container>
        </div>
    )
}

export default HomePage