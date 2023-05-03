import React, { useState } from "react";
import { Link, useHistory } from "react-router-dom";
import Title from "../Title/title";
import { useTopics, useCreateThread } from "../hooks";
import { style } from "./newthreadpage-style";

export default function NewThreadPage() {
  const classes = style();
  const topics = useTopics();
  const [ title, setTitle ] = useState("");
  const [ category, setCategory ] = useState("");
  const [ body, setBody ] = useState("");
  const createThread = useCreateThread();
  const [ error, setError ] = useState()
  const history = useHistory();

  const submitForm = async () => {
    if (!title || !category || !body) {
      setError("Please fill in all the fields");
      return;
    }

    const resp = await createThread({ title, category, body });

    if (resp.status >= 200 && resp.status < 300) {
      const respJson = await resp.json();
      history.push(`/smatch/forum/${respJson.thread_id}`);
    } else {
      setError("There was an error creating the thread. Please try again later");
    }
  };

  return (
    <div className={classes.root}>
      <Title backTo="/smatch/forum">
        Create a New Thread
      </Title>

      <div className={classes.formContainer}>
        <input type="text" className={classes.input} placeholder="Title *" required value={title} onChange={(e) => setTitle(e.target.value)} />

        <select className={classes.select} value={category} required onChange={(e) => setCategory(e.target.value)}>
          <option value="-1">Select category *</option>
          { topics ? (
              topics.map((topic) => <option key={topic || "Other"} value={topic || "Other"}>{ topic || "Other" }</option>)
            ) :
            <></>
          }
        </select>

        <textarea className={classes.textarea} placeholder="Body *" required value={body} onChange={(e) => setBody(e.target.value)}></textarea>

        { error && (
          <p className={classes.error}>
            {error}
          </p>
        )}

        <button className={classes.submitButton} onClick={submitForm}>
          Create Thread
        </button>
      </div>
    </div>
  );
};