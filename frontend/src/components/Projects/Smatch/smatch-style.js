import { makeStyles } from '@material-ui/core/styles';

const smatchStyle = makeStyles(theme => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'space-between',
    minHeight: '200px',
  },
  container: {
    minHeight: '200px',
    display: 'flex',
    justifyContent: 'center',
  },
  bottomNav: {
    position: 'fixed',
    bottom: 20,
    display: 'inline-flex',
    height: '48px',
    width: '200px',
    backgroundColor: '#212121',
    borderRadius: '8px',
    justifyContent: 'center',
    alignItems: 'center',
    gap: '24px',
    padding: '0px 32px',
    border: '2px solid #fff',
  },
}));

export default smatchStyle;