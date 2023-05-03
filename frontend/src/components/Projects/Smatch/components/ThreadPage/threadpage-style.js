import { makeStyles } from '@material-ui/core/styles';

export const style = makeStyles((theme) => ({
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
  threadBox: {
    background: "#212121",
    borderRadius: "50px",
    padding: "10px",
    display: "grid",
    gap: "8px",
    alignItems: "center",
    textDecoration: "none",
    minHeight: '150px',
    width: '80%',
    margin: 'auto'
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
    padding: "16px",
    color: "#fff",
  },
  threadTitleContainer: {
    display: "flex",
    flexDirection: "row",
    alignItems: 'center',
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
  replayIcon: {
    '& img': {
      filter: 'invert(100%)',
      width: '30px',
      height: '30px',
      marginRight: '10px'
    }
  },
  formTextArea: {
    width: '100%',
    height: '150px',
    margin: '10px 0',
    borderRadius: '10px',
    border: 'none',
    padding: '5px',
    outline: 'none'
  },
  formSendButton: {
    width: '120px',
    height: '50px',
    marginTop: '10px',
    border: 'none',
    outline: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    color: '#fff',
    fontWeight: 'bold',
    background: '#c77c00',
    fontSize: '1rem',
  },
  disabledBtn: {
    background: 'gray',
    cursor: 'default',
  }
}));