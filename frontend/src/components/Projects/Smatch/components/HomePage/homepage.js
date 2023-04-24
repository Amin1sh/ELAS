import React from "react";
import { Link } from "react-router-dom";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import Title from "../Title/title";
import { useTopics } from "../hooks";
import { style } from "./style";

function Explore() {
  const classes = style();
  const topics = useTopics();

  return (
    <div className={classes.container}>
      <Title>
        Explore<br />Topics and Skills
      </Title>

      <div className={classes.grid}>
        {topics ? (
          topics.map(topic => (
            <Link
              key={topic || "Other"}
              to={`/smatch/match/${encodeURIComponent(topic)}`}
              className={classes.link}
            >
              {topic || "Other"}
            </Link>
          ))
        ) : (
          <></>
        )}
      </div>
    </div>
  );
}

export default Explore;
