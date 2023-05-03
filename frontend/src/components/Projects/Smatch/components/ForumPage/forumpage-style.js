import { makeStyles } from '@material-ui/core/styles';

const style = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    flex: 1,
  },
  mainContainer: {
    width: '100%',
    maxWidth: 'xl',
    display: 'flex',
    flexDirection: 'column',
    padding: '16px',
    paddingTop: '32px',
    gap: '16px',
    position: 'relative'
  },
  newThreadButton: {
    position: "absolute",
    top: "-12px",
    right: "4px",
    fill: "#FFC107",
    width: "40px",
    height: "40px",
    '& img': {
      width: "40px",
      height: "40px",
      filter: 'invert(60%) sepia(100%) saturate(10000%) hue-rotate(57deg) brightness(2.5) contrast(1.2)'
    }
  },
  threadLink: {
    background: "#212121",
    borderRadius: "50px",
    padding: "10px",
    display: "grid",
    gap: "8px",
    alignItems: "center",
    textDecoration: "none",
    height: '230px',
    width: '100'
  },
  threadIconContainer: {
    gridColumn: "1 / 2",
    aspectRatio: "1/1",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    '& img': {
      width: "100%",
      filter: 'invert(60%) grayscale(100%) brightness(2) contrast(1.2) sepia(100%) hue-rotate(40deg)'
    }
  },
  threadIcon: {
    height: "40px",
    width: "40px",
    fill: "#9E9E9E",
  },
  threadDetailsContainer: {
    display: "flex",
    flexDirection: "column",
    height: "100%",
    gridColumn: "2 / 6",
    padding: "0 16px",
    color: "#fff",
  },
  threadTitleContainer: {
    display: "flex",
    flexDirection: "column",
    flex: 1,
  },
  threadTitle: {
    fontSize: "2rem",
  },
  threadSubtitle: {
    fontSize: "1rem",
  },
  threadMetaData: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    fontSize: "1rem",
  },
}));

export default style;