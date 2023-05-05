import { makeStyles } from '@material-ui/core/styles';

const style = makeStyles((theme) => ({
    root: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        flexGrow: 1,
      },
      title: {
        marginBottom: '32px',
      },
      link: {
        display: 'flex',
        alignItems: 'center',
        backgroundColor: '#ffa500',
        borderRadius: '9999px',
        padding: '16px',
        '& span': {
          color: '#fff',
        },
        textDecoration: 'none',
        justifyContent: 'center',
        textAlign: 'center',
        color: '#fff'
      },
      paper: {
        minWidth: '60%',
        margin: '32px',
        padding: '32px',
        display: 'grid',
        gap: '32px',
        gridTemplateColumns: 'auto',
      },
      noMatch: {
        width: '100%',
        marginTop: '64px',
        borderRadius: '25px',
        backgroundColor: '#212121',
        color: '#fff',
        padding: '32px',
        display: 'flex',
      },
      exploreBtn: {
        backgroundColor: '#ffa500',
        '&:hover': {
          backgroundColor: '#ffa500',
        },
        borderRadius: '9999px',
        padding: '16px',
        flex: 1,
        textAlign: 'center',
        textDecoration: 'none',
        color: '#fff'
      },

      historyTitle: {
        width: '100%',
        height: '60px',
        background: 'gray',
        marginTop: '40px',
        marginBottom: '-40px',
        color: '#fff',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontWeight: 'bold',
        fontSize: '16px',
        borderRadius: '30px',
      },

      flexCol: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
      }
}));

export default style;