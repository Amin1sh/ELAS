import { makeStyles } from "@material-ui/core/styles";

export const style = makeStyles(theme => ({
  container: {
    display: "flex",
    flexDirection: "column",
  },
  searchBox: {
    margin: '10px 145px',
    marginTop: '35px',
    backgroundColor: "#fff",
    borderRadius: '25px',
    '& .MuiOutlinedInput-root': {
      borderRadius: '25px',
    }
  },
  grid: {
    display: "grid",
    gridTemplateColumns: '1fr 1fr',
    [theme.breakpoints.up("lg")]: {
      gridTemplateColumns: '1fr 1fr 1fr',
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
