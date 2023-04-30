import React from 'react';
import { Container, Box } from '@material-ui/core';
import { Switch, Route, Redirect } from 'react-router-dom';

import smatchStyle from './smatch-style';
import NavigationItem from './components/NavigationItem/NavigationItem';

import HomePage from './components/HomePage/homepage';
import ForumPage from './components/ForumPage/forumpage';
import MatchesPage from './components/MatchesPage/matchespage';
import FindMatchPage from './components/FindMatchPage/findmatchpage';
import VisualizationPage from './components/VisualizationPage/visualizationpage';

const HomeIcon = () => <img src="icons/home.svg" />;
const MessageIcon = () => <img src="icons/message.svg" />;
const ViewListIcon = () => <img src="icons/view-list.svg" />;
const ChartBarIcon = () => <img src="icons/chart-bar.svg" />;

export default function Smatch() {
  const classes = smatchStyle();

  return (
    <div className={classes.root}>
      <Container className={classes.container}>
        {/* Content */}
        <Box flex={1}>
          <Switch>
            <Route exact path="/smatch" component={HomePage} />
            <Route path="/smatch/matches" component={MatchesPage} />
            <Route path="/smatch/forum" component={ForumPage} />
            <Route path="/smatch/visualization" component={VisualizationPage} />
            <Route
              exact
              path="/smatch/match/:path*"
              render={(props) => <FindMatchPage {...props} />}
            />
            <Redirect to="/" />
          </Switch>
        </Box>

        {/* Bottom Navigation */}
        <div className={classes.bottomNav}>
          <NavigationItem icon={<HomeIcon />} to="/smatch" />
          <NavigationItem icon={<ViewListIcon />} to="/smatch/matches" />
          <NavigationItem icon={<MessageIcon />} to="/smatch/forum" />
          <NavigationItem icon={<ChartBarIcon />} to="/smatch/visualization" />
        </div>
      </Container>
    </div>
  );
}