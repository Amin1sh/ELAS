import React from "react";
import { Link } from "react-router-dom";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import { withStyles } from "@material-ui/core/styles";
import style from "./style";

class Title extends React.Component {
  render() {
    const { children, subtitle, backTo, classes } = this.props;
    return (
      <div className={classes.root}>
        {backTo ? (
          <Link to={backTo} className={classes.link}>
            <ChevronLeftIcon />
          </Link>
        ) : (
          <></>
        )}
        <h1 className={classes.title}>{children}</h1>
        {subtitle ? (
          <span className={classes.subtitle}>{subtitle}</span>
        ) : (
          <div style={{ paddingBottom: "16px" }}></div>
        )}
      </div>
    );
  }
}

export default withStyles(style)(Title);