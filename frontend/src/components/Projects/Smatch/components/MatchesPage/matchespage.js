import React, { useContext } from "react"
import { Link } from "react-router-dom";

import Title from "../Title/title";
import { useGetHistory } from "../hooks";

import style from "./matchespage-style";

export default function MatchesPage() {
  const matches_history = useGetHistory();

  const classes = style();

  return (
    <div className={classes.root}>
      <Title>
        {(matches_history && matches_history.length > 0) ? "It's a Match!" : "You have no matches yet!"}
      </Title>

      {(matches_history && matches_history.length > 0) ? (
        <div>
          {matches_history.map((history) => (
            <div className={classes.flexCol}>
              <div className={classes.historyTitle}>
                {history.topic} • {history.created_on}
              </div>

              <div className={classes.paper}>
                {
                  (JSON.parse(history.result).length > 0) ?
                    JSON.parse(history.result).map((item) => (
                    <Link
                      key={item.course_id}
                      className={classes.link}
                      to={`/smatch/course/${item.course_id}`}
                    >
                      <span>{item.subject}</span>
                    </Link>
                  )) : 
                  <div className={classes['not-found-match']}>
                    <p>Sorry, there is no match according to your interest, you can try again.</p>
                  </div>
                }
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className={classes.noMatch}>
          <Link className={classes.exploreBtn} to="/smatch/">
            Explore topics and skills
          </Link>
        </div>
      )}
    </div>
  )
}