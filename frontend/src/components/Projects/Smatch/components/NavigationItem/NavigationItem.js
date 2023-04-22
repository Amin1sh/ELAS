import React from 'react';
import { Link, useRouteMatch } from 'react-router-dom';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Badge from '@material-ui/core/Badge';
import styles from './navigationitem-styles';

function NavigationItem({ classes, icon, to, badge }) {
  const match = useRouteMatch(to);

  const isActive = match && match.isExact;

  return (
    <Link to={to} className={`${classes.root} ${isActive ? "active" : ""}`}>
      {React.cloneElement(icon, { className: 'w-full h-full' })}
      {badge ? (
        <Badge
          classes={{ badge: classes.badge }}
          badgeContent={badge}
        />
      ) : (
        <></>
      )}
    </Link>
  );
}

NavigationItem.propTypes = {
  classes: PropTypes.object,
  icon: PropTypes.element.isRequired,
  to: PropTypes.string.isRequired,
  badge: PropTypes.string,
};

export default withStyles(styles)(NavigationItem);