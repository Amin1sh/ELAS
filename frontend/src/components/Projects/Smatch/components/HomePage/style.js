import { makeStyles } from "@material-ui/core/styles";

export const style = makeStyles(theme => ({
  container: {
    display: "flex",
    flexDirection: "column",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: 'auto auto',
    [theme.breakpoints.up("lg")]: {
      gridTemplateColumns: 'auto auto auto',
    },
    gap: '24px',
    padding: '16px',
    paddingTop: '48px',
  },
  link: {
    textDecoration: 'none',
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    backgroundColor: '#212121',
    color: '#fff',
    borderRadius: "999px",
    cursor: "pointer",
    padding: '8px',
  },
}));
