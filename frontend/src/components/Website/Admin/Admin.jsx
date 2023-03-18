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

  /* udemy */
  const [udemyScrapeState, handleUdemyScrape] = useState("checking...")
  const [udemyOpenScrapeDialog, setUdemyOpenScrapeDialog] = useState(false)
  const [udemyPage, setUdemyPage] = useState(1)

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


      fetch(`${process.env.REACT_APP_BASE_URL}/udemy_scraping`)
        .then((response) => response.json())
        .then((data) => {
          handleUdemyScrape(data.statusMessage);
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

  const doUdemyScrape = (e) => {
    e.preventDefault();
    e.target.reset();

    fetch(`${process.env.REACT_APP_BASE_URL}/udemy_scraping`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        udemy_pagenumber: udemyPage
      }),
    });
    handleUdemyScrape("running...");
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
              <Button
                variant="contained"
                color="primary"
                size="small"
                className={classes.button}
                disabled={
                  udemyScrapeState === "running..." ||
                  udemyScrapeState === "checking..."
                }
                type="button"
                onClick={() => setUdemyOpenScrapeDialog(!udemyOpenScrapeDialog)}
              >
                Udemy Scrape courses
              </Button>
            </Grid>
            <Grid item>
              <Typography variant="body1" style={{ paddingLeft: 12 }}>
                Udemy Last scraped: {udemyScrapeState}
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







      <Dialog
        open={udemyOpenScrapeDialog}
        onClose={() => setUdemyOpenScrapeDialog(!udemyOpenScrapeDialog)}
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
              <form onSubmit={doUdemyScrape}>
                <TextField
                  id="udemy_page"
                  label="Udemy Page Number (1, 2, 3, etc ..."
                  required
                  fullWidth
                  type="number"
                  InputProps={{
                    inputProps: { 
                        max: 1000, min: 1
                    }
                  }}
                  onChange={(e) => setUdemyPage(e.target.value)}
                  // disabled={(udemyScrapeState === "running..." || udemyScrapeState === "checking...")}
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
                      udemyScrapeState === "running..." ||
                      udemyScrapeState === "checking..."
                    }
                    type="submit"
                  >
                    Scrape Now
                  </Button>
                  <p style={{ paddingLeft: 12 }}>Last scraped: {udemyScrapeState}</p>
                </Grid>
              </form>
            </Grid>
          </Grid>
        </DialogContent>
      </Dialog>
    </>
  );
}
