import React from "react"
import { Link } from "react-router-dom";

import Title from "../Title/title";
import { useThreads, useUserCount } from "../hooks";
import style from "./forumpage-style";

const PlusIcon = () => <img src="/icons/plus-circle.svg" />;
const ForumIcon = () => <img src="/icons/forum.svg" />;

export default function ForumPage() {
  const classes = style();
  const threads = useThreads();
  const userCount = useUserCount();

  return (
    <div className={classes.root}>
      <Title subtitle={`${userCount || 0} Members`}>Forum</Title>

      <div className={classes.mainContainer}>
        <Link to="/smatch/forum/new" className={classes.newThreadButton}>
          <PlusIcon />
        </Link>

        {threads &&
          threads.map((thread) => (
            <Link
              key={thread.id}
              to={`/smatch/forum/${thread.id}`}
              className={classes.threadLink}
            >
              <div className={classes.threadIconContainer}>
                <ForumIcon className={classes.threadIcon} />
              </div>

              <div className={classes.threadDetailsContainer}>
                <div className={classes.threadTitleContainer}>
                  <span>
                    {thread.email} • {thread.category}
                  </span>
                  <h3 className={classes.threadTitle}>{thread.title}</h3>
                </div>
                <div className={classes.threadMetaData}>
                  <span>
                    {`${thread.replies} ${thread.replies <= 1 ? 'Reply' : 'Replies'}`}
                  </span>
                  <span>{thread.last_reply_on}</span>
                </div>
              </div>
            </Link>
          ))}
      </div>
    </div>
  )
}