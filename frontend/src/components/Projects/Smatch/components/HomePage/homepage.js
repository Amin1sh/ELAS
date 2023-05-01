import React, {useState} from "react";
import SearchIcon from "@material-ui/icons/Search";
import {InputAdornment, TextField} from "@material-ui/core";
import { Link } from "react-router-dom";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import Title from "../Title/title";
import { useTopics } from "../hooks";
import { style } from "./style";

function Explore() {
  const classes = style();
  const topics = useTopics();

  const [topicSearch, setTopicSearch] = useState("");

  const handleTopicSearch = (event) => {
    setTopicSearch(event.target.value);
  };

  return (
    <div className={classes.container}>
      <Title>
        Explore<br />Topics and Skills
      </Title>

      <TextField className={classes.searchBox}
        placeholder="Search for topics" value={topicSearch} onChange={handleTopicSearch}
        variant="outlined" InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <SearchIcon style={{color: "#909090"}}/>
          </InputAdornment>
        ),
      }}
      />

      <div className={classes.grid}>
        {topics ? (
          topics.filter(topic => topic.toLowerCase().split(' ').some(word => word.startsWith(topicSearch.toLowerCase()))).map(topic => (
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
