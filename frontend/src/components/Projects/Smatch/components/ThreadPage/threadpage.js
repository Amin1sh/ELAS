import React, { useState } from "react"
import { Link, useParams } from "react-router-dom";

import Title from "../Title/title";
import { useThread, useCreateReply } from "../hooks";
import {style} from "./threadpage-style";

const ReplyIcon = () => <img src="/icons/reply.svg" />;

export default function ThreadPage() {
    const classes = style();
    const { thread_id } = useParams();
    const { thread, refresh } = useThread(thread_id);

    const [ body, setBody ] = useState("");
    const createReply = useCreateReply(thread_id);

    const submitForm = async () => {
        if(body) {
          await createReply({ body });
          setBody("");
          refresh();
        }
    };

    return thread ? (
    <div className={classes.root}>
        <Title subtitle={`${thread.email} • ${thread.category}`}>{thread.title}</Title>

        <div className={classes.mainContainer}>
            <div className={classes.threadBox}>
                <div className={classes.threadDetailsContainer}>
                    <div className={classes.threadTitleContainer}>
                        {thread.body}
                    </div>
                    <div className={classes.threadMetaData}>
                        <span>
                        </span>
                        <span>{thread.created_on}</span>
                    </div>
                </div>
            </div>

            {
                thread.replies.map(reply => (
                    <div className={classes.threadBox}>
                        <div className={classes.threadDetailsContainer}>
                            <div className={`${classes.threadTitleContainer} ${classes.replayIcon}`}>
                                <ReplyIcon />
                                <span>{reply.email}</span>
                            </div>
                            <div className={classes.threadMetaData}>
                                {reply.body}
                            </div>

                            <div className={classes.threadMetaData}>
                                <span>
                                </span>
                                <span>{reply.created_on}</span>
                            </div>
                        </div>
                    </div>
                ))
            }

            <div className={classes.threadBox}>
                <div className={classes.threadDetailsContainer}>
                    <div className={`${classes.threadTitleContainer} ${classes.replayIcon}`}>
                        <ReplyIcon />
                        <span>you</span>
                    </div>
                    <div className={classes.threadMetaData}>
                        <textarea className={classes.formTextArea} value={body} onChange={(e) => setBody(e.target.value)} />
                    </div>

                    <button disabled={!body} className={`${classes.formSendButton} ${!body ? classes.disabledBtn : ''}`} onClick={() => submitForm()}>Post</button>
                </div>
            </div>
        </div>
    </div>
    ):
    <></>
}