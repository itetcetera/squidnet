import logo from './Squidnet_logo.png';

import {
  BrowserRouter as Router,
  Switch,
  Route
} from 'react-router-dom'
import 'semantic-ui-css/semantic.min.css'
import HomePage from "./core/homepage"
import NetworkPage from './core/networking';
import Websocker from './core/websocket';

function App() {
  return (
    <Router>
      <Switch>
        <Route path='/networking'>
          <NetworkPage />
        </Route>
        <Route exact path="/websocket">
          <Websocker />
        </Route>
      </Switch>
    </Router>

  );
}

export default App;
