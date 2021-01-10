import logo from './Squidnet_logo.png';

import {
  BrowserRouter as Router,
  Switch,
  Route
} from 'react-router-dom'
import 'semantic-ui-css/semantic.min.css'
import HomePage from "./core/homepage"

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <HomePage />
        </Route>
      </Switch>
    </Router>

  );
}

export default App;
