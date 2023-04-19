import React, { useEffect, useState } from "react";
import { Dialog, DialogContent, Typography } from "@material-ui/core";
import CssBaseline from "@material-ui/core/CssBaseline";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import ArrowForwardIcon from "@material-ui/icons/ArrowForward";

const useStyles = makeStyles((theme) => ({
  root: {
    height: "100vh",
    marginTop: theme.spacing(4),
  },
  button: {
    borderRadius: theme.spacing(1, 0.25, 1, 0.25),
  },
  y_padding: {
    paddingTop: "10px",
    paddingBottom: "10px"
  }
}));

export default function Admin(props) {
  const classes = useStyles();
  const [scrapeState, handleScrape] = useState("checking...");

  const [openScrapeDialog, setOpenScrapeDialog] = useState(false);
  const [e3, sete3] = useState("");
  const [insight, setinsight] = useState("");

  
  /* edx */
  const [edxScrapeState, handleEdxScrape] = useState("checking...")

  /* coursera */
  const [courseraScrapeState, handleCourseraScrape] = useState("checking...")


  useEffect(() => {
    let interval = setInterval(() => {
      fetch(`${process.env.REACT_APP_BASE_URL}/commence_scraping`)
        .then((response) => response.json())
        .then((data) => {
          handleScrape(data.statusMessage);
        })
        .catch((error) => {
          console.log(error);
        });


      

        fetch(`${process.env.REACT_APP_BASE_URL}/edx_scraping`)
        .then((response) => response.json())
        .then((data) => {
          handleEdxScrape(data.statusMessage);
        })
        .catch((error) => {
          console.log(error);
        });

        fetch(`${process.env.REACT_APP_BASE_URL}/coursera_scraping`)
        .then((response) => response.json())
        .then((data) => {
          handleCourseraScrape(data.statusMessage);
        })
        .catch((error) => {
          console.log(error);
        });


    }, 2500);
    return () => clearInterval(interval);
  });


  const doScrape = (e) => {
    e.preventDefault();
    e.target.reset();

    fetch(`${process.env.REACT_APP_BASE_URL}/commence_scraping`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        e3: e3,
        insight: insight,
      }),
    });
    handleScrape("running...");
  };

  

  const doEdxScrape = (e) => {
    e.preventDefault();
    e.target.reset();

    fetch(`${process.env.REACT_APP_BASE_URL}/edx_scraping`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    handleEdxScrape("running...");
  };


  const doCourseraScrape = (e) => {
    e.preventDefault();
    e.target.reset();

    fetch(`${process.env.REACT_APP_BASE_URL}/coursera_scraping`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    handleCourseraScrape("running...");
  };

  return (
    <>
      <Grid container component="main" className={classes.root}>
        <CssBaseline />
        <Grid item xs={false} md={2} />
        <Grid item xs={12} md={8} square>
          <Typography gutterBottom variant="h3">
            Welcome, Admin!
          </Typography>

          <Grid container alignItems="center" className={classes.y_padding}>
            <Grid item>
              <Button
                variant="contained"
                color="primary"
                size="small"
                className={classes.button}
                /* !True -> False, !False -> True */
                onClick={() => setOpenScrapeDialog(!openScrapeDialog)}
              >
                Scrape courses
              </Button>
            </Grid>
            <Grid item>
              <Typography variant="body1" style={{ paddingLeft: 12 }}>
                Last scraped: {scrapeState}
              </Typography>
            </Grid>
          </Grid>

         


          <hr/>

          <Grid container alignItems="center" className={classes.y_padding}>
            <Grid item>
            <form onSubmit={doEdxScrape}>
              <Button
                variant="contained"
                color="primary"
                size="small"
                className={classes.button}
                disabled={
                  edxScrapeState === "running..." ||
                  edxScrapeState === "checking..."
                }
                type="submit"
              >
                EDX Scrape courses
              </Button>
              </form>
            </Grid>
            <Grid item>
              <Typography variant="body1" style={{ paddingLeft: 12 }}>
                EDX Last scraped: {edxScrapeState}
              </Typography>
            </Grid>
          </Grid>


          <hr/>

          <Grid container alignItems="center" className={classes.y_padding}>
            <Grid item>
              <form onSubmit={doCourseraScrape}>
                <Button
                  variant="contained"
                  color="primary"
                  size="small"
                  className={classes.button}
                  disabled={
                    courseraScrapeState === "running..." ||
                    courseraScrapeState === "checking..."
                  }
                  type="submit"
                >
                  Coursera Scrape courses
                </Button>
              </form>
            </Grid>
            <Grid item>
              <Typography variant="body1" style={{ paddingLeft: 12 }}>
                Coursera Last scraped: {courseraScrapeState}
              </Typography>
            </Grid>
          </Grid>

        </Grid>
        <Grid item xs={false} md={2} />
      </Grid>

      <Dialog
        open={openScrapeDialog}
        onClose={() => setOpenScrapeDialog(!openScrapeDialog)}
        fullWidth={true}
        maxWidth="sm"
      >
        <DialogContent style={{ height: 225 }}>
          <Grid
            container
            direction="column"
            alignItems="center"
            justify="center"
          >
            <Grid item>
              <form onSubmit={doScrape}>
                <TextField
                  id="e3url"
                  label="E3 Courses address link (LSF)"
                  required
                  fullWidth
                  onChange={(e) => sete3(e.target.value)}
                  // disabled={(scrapeState === "running..." || scrapeState === "checking...")}
                />
                <TextField
                  id="insighturl"
                  label="StudyCompass address link (LSF)"
                  required
                  fullWidth
                  onChange={(e) => setinsight(e.target.value)}
                  // disabled={(scrapeState === "running..." || scrapeState === "checking...")}
                />
                <Grid
                  container
                  direction="row"
                  spacing={5}
                  alignItems="center"
                  justify="flex-start"
                  style={{ marginTop: 36, paddingLeft: 18 }}
                >
                  <Button
                    variant="contained"
                    color="primary"
                    className={classes.button}
                    endIcon={<ArrowForwardIcon />}
                    disabled={
                      scrapeState === "running..." ||
                      scrapeState === "checking..."
                    }
                    type="submit"
                  >
                    Scrape Now
                  </Button>
                  <p style={{ paddingLeft: 12 }}>Last scraped: {scrapeState}</p>
                </Grid>
              </form>
            </Grid>
          </Grid>
        </DialogContent>
      </Dialog>


      
      
      
    </>
  );
}
